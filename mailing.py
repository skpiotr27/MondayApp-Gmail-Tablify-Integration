from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json
import base64
import os


def send_email(subject,message_text,email,sender,cc_email):
    
    with open('download_data/credentials.json') as f:
        credentials_info = json.load(f)
        print(credentials_info)

    # Utworzenie Credentials na podstawie wczytanych danych
    credentials = Credentials.from_authorized_user_info(credentials_info)

    # Utwórz klienta Gmail API
    service = build('gmail', 'v1', credentials=credentials)

    # Tworzenie wiadomości
    message = MIMEMultipart()
    message['to'] = email
    message['from'] = sender
    message['subject'] = subject
    message.attach(MIMEText(message_text, 'html'))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    # Wysłanie maila
    message = (service.users().messages().send(userId='me', body={'raw': raw_message})
            .execute())
    print(f"Wiadomość wysłana. Identyfikator wiadomości: {message['id']}")

    return True

def send_email_with_attachments(subject,message_text,email,sender,file_path,cc_email):
    
        with open('download_data/credentials.json') as f:
            credentials_info = json.load(f)

        # Utworzenie Credentials na podstawie wczytanych danych
        credentials = Credentials.from_authorized_user_info(credentials_info)

        # Utwórz klienta Gmail API
        service = build('gmail', 'v1', credentials=credentials)

        # Tworzenie wiadomości
        message = MIMEMultipart()
        message['to'] = email
        message['cc'] = cc_email
        message['from'] = sender
        message['subject'] = subject
        
        with open('messages/footer.html', 'r',encoding='utf8') as f:
            footer = f.read()

        message_text += footer
        
        message.attach(MIMEText(message_text, 'html',_charset='utf-8'))
        
        part = MIMEBase('application',"octet-stream")
        part.set_payload(open(file_path,"rb").read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(file_path))
        message.attach(part)
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        # Wysłanie maila
        message = (service.users().messages().send(userId='me', body={'raw': raw_message})
                .execute())
        print(f"Wiadomość wysłana. Identyfikator wiadomości: {message['id']}")

        return True