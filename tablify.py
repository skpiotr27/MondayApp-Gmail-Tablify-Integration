import requests
from decouple import config
import json
from urllib.parse import urlparse
import os

api_key = config('TABLIFY_API')
secret_key = config('TABLIFY_SECRET')

def get_item(table_id,item_id):
    
    url = f"https://tablify.app/api/table/{table_id}/rows"
    query_params = {
        "quickSearchQuery": str(item_id),
    }

    try:
        response = requests.get(url,params=query_params,auth=(api_key,secret_key))
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Wystąpił błąd podczas przesylania żądania: {e}")
        return {e}
      
def get_list_files(column_id,row_id):
    
    url = f"https://tablify.app/api/cell/{column_id}:{row_id}/file-items?limit=100&offset=0"
    
    try:
        response = requests.get(url,auth=(api_key,secret_key))
        response.raise_for_status()
        response_data = response.json()
        with open('get_list_files.json', 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Wystąpił błąd podczas przesylania żądania: {e}")
        return {e} 
    
def download_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response 
    except requests.exceptions.RequestException as e:
        return f"Error occurred{e}"
    
def get_file_extension(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    file_extension= os.path.splitext(path)[-1]
    return file_extension

def get_file_name(response):
    content_disposition = response.headers.get('Content-Disposition')
    print(content_disposition)
    if content_disposition:
        _, params = content_disposition.split(";")
        for param in params.split(";"):
            key, value = param.strip().split("=")
            if key == "filename":
                return value.strip("\"'")
    return None

def get_file_name_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    file_name = os.path.basename(path)
    return file_name

table_id = '6269c012735e1a0a9a12adc0' 
item_id = 24770
column_id = '6269f28d6c54f4fd942eea70'
row_id = '62792c5ef68c04b5cccea040'

""" items = get_list_files(column_id,row_id)

for item in items['data']['cellFileItems']:
    file_url = item['file']['url']
    print(file_url) """
    
""" url = 'https://toolify.eu-central-1.linodeobjects.com/files/62734b287902cafa6943dc96-5bubtahy4Ec220xgUxZUMHcSmhPOs9nuoeKW0KkXTCEYGgOdImy1hDDLnEw0X42JJ31kaSDzIvl60vwB0YAMuCTkr0kw4dGhhmTZW4NyNLyilwmfznXEyjKzHusPhhj7.pdf'
files = download_file(url)

if isinstance(files,str):
    print(files)
else:
    file_name = get_file_name(files)

    
    if not file_name:
        file_name = get_file_name_from_url(url)
    
    folder_path = "download_data"
    file_path = os.path.join(folder_path,file_name)
    
    
    with open(file_path, 'wb') as file:
        file.write(files.content)
        print(f"Plik został pomyślnie pobrany i zapisany jako: {file_path}") """
