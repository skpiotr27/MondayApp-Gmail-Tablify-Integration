import os
import json
from mailing import send_email,send_email_with_attachments
from monday import change_column_value, get_board_columns,get_boards,find_items_by_column_value, get_item_columns,create_update
from tablify import get_file_extension, get_file_name,get_file_name_from_url,get_item,get_list_files,download_file
from string import Template
from logs import error,success
import datetime
from email_validator import validate_email, EmailNotValidError

# Function which search client on tablify, search column and file, downloading file and save in folder \attachments
def tablify_process(item_id, name_value):
    try:
        tablify_item = get_item(table_id='6269c012735e1a0a9a12adc0', item_id=item_id)
        cellFileItems = tablify_item["data"]["rows"]
        if len(cellFileItems) == 0:
            raise ValueError ("Nie znaleziono klienta na Tablify")

        
        tablify_row_id = tablify_item["data"]["rows"][0]["id"]
        if tablify_row_id is None:
            raise ValueError ("Nie znaleziono id wiersza klienta na Tablify")

        tablify_files = get_list_files(column_id="640b3728e9acd54febe77a69", row_id=tablify_row_id)
        if tablify_files is None:
            raise ValueError ("Brak plików na Tablify")

        cellFileItems = tablify_files["data"]["cellFileItems"]
        if len(cellFileItems) == 0:
            raise ValueError("Brak plików na Tablify")
        tablify_file_url = cellFileItems[0]["file"]["url"]

        tablify_file_title = tablify_files["data"]["cellFileItems"][0]["title"]
        if tablify_file_title is None:
            tablify_file_title = "File"
            error(error_message="UWAGA - brak nazwy pliku", name_value=name_value)            

        files = download_file(tablify_file_url)

        folder_path = "attachments"
        file_extension = get_file_extension(tablify_file_url)
        file_name = "Projekt instalacji.pdf"
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'wb') as file:
            file.write(files.content)
            print(f"Plik został pomyślnie pobrany i zapisany jako: {file_path}")

        return True, file_path   # Zwraca True, gdy wszystko przebiegnie pomyślnie
    except ValueError as e:
        print(e)
        error(error_message=e, name_value=name_value)
        file_path = ""
        return False, file_path  # Zwraca False, gdy wystąpi błąd  



# Function which download data from Monday, and returned True/False when all required columns exist, returned value of columns
def download_data_from_monday(item_data):
    item_id = None
    email = None
    uwagi = None
    try:
        for column_value in item_data["column_values"]:
            if column_value["id"] == "id_umowy":
                item_id = column_value["value"]
                if item_id is None:
                    continue
                item_id = item_id.strip('"')
                    
            elif column_value["id"] == "e_mail8":
                email = column_value["value"]
                if email is None:
                    continue
                email = email.strip('"')
                    
            elif column_value["id"] == "long_text9":
                uwagi = column_value["value"]
                if uwagi is None:
                    uwagi = ""
                uwagi = uwagi.strip('"')
                
            elif column_value["id"] =="dup__of_produkt2":
                pakiet = column_value["text"]
                if pakiet is None:
                    pakiet = ""
                pakiet = pakiet.strip('"')
            elif column_value["id"] == "handlowiec5":
                handlowiec = column_value["text"]
                if handlowiec is None:
                    handlowiec = ""
                handlowiec = handlowiec.strip('"')
                
        if item_id is None:
           raise ValueError("Brak ID klienta")
        if email is None:
            raise ValueError("Brak adresu email")

        if item_id and email:
            return True, item_id, email, uwagi,pakiet,handlowiec
        else:
            return False, None, None, None, None
        
    except ValueError as e:
        print(e)
        error(error_message=e,name_value=name_value)
        uwagi = ""
        email = ""
        item_id = ""
        pakiet = ""
        handlowiec = ""
        return False,None,None,None,None,None

# Function downloaded email adress of seller
def get_seller_email(handlowiec,name_value):
    try:
        item = find_items_by_column_value(board_id='421462032',column_id='name',column_value=handlowiec)
        
        for item_data in item["data"]["items_by_column_values"]:
            for column_value in item_data["column_values"]:
                if column_value["id"] == "text57":
                    email = column_value["text"] 
                    if email is None:
                        continue
            if email is None:
                raise ValueError ("Brak maila DTH")
            if email:
                return email
    except ValueError as e:
        print(e)
        error(error_message=e,name_value=name_value)
        email = ""
        return email

# Opening template of mail message 
with open('messages/projekt.html','r',encoding='utf8') as file:
        html_template = file.read()
        template = Template(html_template) 
        

# Searching items only with status "Do wysłania"   
item = find_items_by_column_value(board_id='1907592970',column_id='status_125',column_value='Do wysłania')


# Iterations for everyone item in downloaded data
for item_data in item["data"]["items_by_column_values"]:
    # Get name_value (name_item) and id_monday (id item from monday)
    name_value = item_data["name"]
    id_monday = item_data["id"]

    # Downloading required columns for searched items
    monday, item_id, email, uwagi, pakiet, handlowiec = download_data_from_monday(item_data)
    
    email_dth = get_seller_email(handlowiec,name_value)
    
    
    # If all required columns is not exist, the iteration is overlooked
    if not monday:
        change_column_value (board_id='1907592970',column_id='status_125',item_id=id_monday,value_to_change='Błąd')
        create_update(item_id=id_monday, text="Projekt nie wysłany - problem z Monday (sprawdź czy wymagane kolumny są uzupełnione[ID Montażu, Email])")
        continue
    
    # Format downloaded data from json string
    email = json.loads(email)
    if uwagi:
        uwagi = json.loads(uwagi)
        uwagi = uwagi['text']  
    email = email['text']
    
    # Verifying whether pakiet include word  "Standard"
    if "Standard" in pakiet:
        pakiet = "Przedstawione w projekcie wartości są symulacją średnich uzysków z instalacji fotowoltaicznej, które uzależnione są w głównej stopniu od warunków pogodowych w ciągu roku, braku zacienienia, czystości modułów oraz innych czynników. Wyznaczone są na podstawie historycznych wartości średniego natężenia promieniowania słonecznego w danym regionie oraz ukierunkowania modułów. Należy jednak pamiętać, że poniższy załącznik jest prognozą."
    else:
        pakiet = ""
        
    # Run tablify process (search client, download file and save it - it's work only for one file)
    tablify, file_path = tablify_process(item_id=item_id, name_value=name_value)
    if not tablify:
        change_column_value (board_id='1907592970',column_id='status_125',item_id=id_monday,value_to_change='Błąd')
        create_update(item_id=id_monday, text="Projekt nie wysłany - problem z Tablify(sprawdź czy wymagane kolumny są uzupełnione [ID Montażu takie samo jak w monday, plik z projektem został załadowany na Tablify])")
        continue
        
    # Preparing variable for email message
    data={
        'pakiet':pakiet,
        'uwagi': uwagi
    }
    # Include variables in the message
    message_text = template.substitute(data)
    
    # Set title of message
    subject = f"Projekt instalacji [{name_value}]" 
    
    try:
        # Validate email adress
        v = validate_email(email)
        # Send mail 
        send_email_with_attachments(subject=subject,message_text=message_text,email=email, sender='piotr.skok@sundaypolska.pl',file_path=file_path,cc_email=email_dth)
        # Remove attachments from local folder
        os.remove(file_path)
        # Change column value for item 
        change_column_value (board_id='1907592970',column_id='status_125',item_id=id_monday,value_to_change='Wysłane')
        create_update(item_id=id_monday, text="Projekt wysłany prawidłowo")
        success(message="Projekt instalacji wysłany",name_value=name_value)
    except EmailNotValidError as e:
        print(e)
        error(error_message="Błędny adres email", name_value=name_value)
        change_column_value (board_id='1907592970',column_id='status_125',item_id=id_monday,value_to_change='Błąd')
        create_update(item_id=id_monday, text="Projekt nie wysłany - błędny adres email klienta")
    




