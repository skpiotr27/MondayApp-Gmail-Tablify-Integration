# Monday.com, Tablify and Gmail Integration

The program I'm presenting is part of a large project for one of the biggest companies in its industry in Poland and Germany. The entire project involves implementing scripts in each department related to process automation. The script I'm presenting is responsible for sending the project to the end client. I invite you to familiarize yourself with the program.

The program functions as follows: After a designer creates a project, they send it to the database (Tablify). Then, in the CRM (Monday.com), the designer marks the project for delivery. Every 10 minutes, the script checks if there are projects to be delivered. If there are, it retrieves customer data from the CRM, searches for the customer and the project file in the database, and then sends the project as an attachment in a personalized email. The client's requirement was to generate logs regarding errors and successes. All logs are saved in the "done_logs" and "error_logs" folders, where each day has a separate TXT file. Additionally, the logs are sent to the CRM so that the designer can immediately see whether the email delivery was successful or encountered an issue.

## Preparing API Connections

To make the function work, we need to prepare Gmail API files, as well as API codes and Secret Key from Tablify and Monday.

### Gmail

To generate Gmail API access, you need to create a project on console.cloud.google.com/ that allows communication with your mailbox. There, you'll be able to download a JSON file. Download it and then save it in the "download_data" folder as "credentials.json". Next, you need to run the get_refresh_token.py file to generate a token, which should be placed in the credentials.json file.

### Tablify and Monday

The client provided access to the databases. If you obtain your API from Monday and the database, you can place them in a .env file and put it in the main directory.

## Description of the functions

### Main.py

This is a very simple function that manages the timing of calling a subfunction: here, projekty.py, which is responsible for the entire process of sending projects. In the original main.py function, many other subfunctions are invoked, each responsible for different tasks, such as sending SMS.



