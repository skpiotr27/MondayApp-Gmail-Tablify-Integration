import requests
import json
from decouple import config

api_token = config('API_TOKEN')

url = 'https://api.monday.com/v2'

headers = {
    'Authorization': api_token,
    'Content-Type': 'application/json'
}

def get_boards():
    query = '''
    {
        boards (limit:200) {
            id
            name
        }
    }
    '''
    data = {'query': query}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        with open('boards.json', 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)
    else:
        response_data = f'Request failed with status code {response.status_code}'
    return response_data

def get_board_columns(board_id):
    query = '''
    {
        boards (ids: %s){
            columns{
                id
                title
            }
        }
        }''' % board_id
    data = {'query': query}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code // 100 == 2:
        response_data = response.json()
        with open('columns.json', 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)
    else:
        response_data = f'Request failed with status code {response.status_code}'
    return response_data

def find_items_by_column_value(board_id, column_id, column_value):
    
    query = '''
    {
        items_by_column_values (
            board_id: %s,
            column_id: "%s",
            column_value: "%s"
        ){
            id
            name
            column_values{
                id
                value
                text
            }
        }
    }
    ''' % (board_id, column_id, column_value)

    data = {'query': query}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        with open('items_new.json', 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)
    else:
        response_data = f'Request failed with status code {response.status_code}'
    return response_data

def get_item_columns(item_id):
    
    query = '''{
                items (ids: 4909424662) {
                    column_values {
                    column {
                        id
                    }
                    id
                    type
                    value
                    }
  }
                }
        '''
    data = {'query':query}
    response = requests.post(url,headers=headers,json=data)
    
    if response.status_code == 200:
        response_data = response.json()
        with open('get_item.json','w', encoding='utf-8') as f:
            json.dump(response_data,f,ensure_ascii=False,indent=2)
    else:
        response_data = f'Request failed with status code {response.status_code}'
    return response_data

def change_column_value(board_id, column_id, item_id, value_to_change):
    query = '''
    mutation {{
        change_simple_column_value (board_id: {board_id},
        item_id: {item_id},
        column_id: {column_id},
        value: "{value_to_change}"){{
            id
        }}
    }}
    '''.format(board_id=board_id, item_id=item_id, column_id=column_id, value_to_change=value_to_change)

    column_values = json.dumps({column_id: {"label": value_to_change}})

    variables = {'myItemID': item_id, 'myColumnValues': column_values}

    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

    if response.status_code == 200:
        print('Zmieniono wartość kolumny.')
    else:
        print(f'Błąd: {response.content}')


def create_update(item_id, text):
    query = '''
    mutation {
        create_update (item_id: %s, body: "%s") {
            id
        }
    }''' % (item_id, text)

    response = requests.post(
        url,
        headers=headers,
        json={'query': query}
    )

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

