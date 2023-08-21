
import datetime
import os


# Function attendant handling an error with save error in logs
def error(error_message,name_value):
    if not os.path.exists('error_logs'):
        os.makedirs('error_logs')
    
    now = datetime.datetime.now()
    
    filename = now.strftime('%d-%m-%Y') + '.txt'
    filepath = os.path.join('error_logs',filename)
    
    with open(filepath,'a') as f:
        f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} - {error_message} - {name_value}\n")
            
    return 0

def success(message,name_value):
    
    if not os.path.exists('done_logs'):
        os.makedirs('done_logs')
        
    now = datetime.datetime.now()
    
    filename = now.strftime('%d-%m-%Y') + '.txt'
    filepath = os.path.join('done_logs',filename)
    
    with open(filepath, 'a') as f:
        f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} - {message} - {name_value}\n")
        
    return 0
        
        