# Integration of Monday.com, Tablify, and Gmail

This repository showcases a comprehensive project tailored for one of the leading firms in both the Polish and German industries. The project's scope encompasses the implementation of scripts across various departments, primarily focusing on process automation. The script highlighted in this repository addresses the task of dispatching projects to end clients. I encourage you to delve into the program and explore its functionalities.

## Workflow Overview

The operation of the program unfolds as follows: Once a designer creates a project, it is dispatched to the database (Tablify). Simultaneously, within the CRM platform (Monday.com), the designer designates the project for delivery. At regular intervals of every 10 minutes, the script assesses if there are pending projects to be sent. If affirmative, the script acquires pertinent customer details from the CRM, locates the customer and the project file within the database, and subsequently transmits the project as an attachment through a customized email. Notably, the client's stipulation necessitated the generation of logs documenting both triumphs and errors. These logs are organized into distinct folders, "done_logs" and "error_logs," with separate text files for each day. Furthermore, these logs are conveyed to the CRM, promptly informing the designer about the success or challenges encountered during email delivery.

## Establishing API Connections

To activate the program's functionality, it is imperative to set up API connections for Gmail, Tablify, and Monday.

### Gmail

Initiating Gmail API access entails creating a project on console.cloud.google.com/, thereby enabling communication with your mailbox. Consequently, a JSON file will be available for download. This downloaded file should be saved in the "download_data" folder and named "credentials.json". Subsequently, running the `get_refresh_token.py` script is essential for generating a token, which must be stored in the `credentials.json` file.

### Tablify and Monday

Access to the databases has been provided by the client. If you procure your API credentials from Monday and the database, these can be conveniently placed within a `.env` file situated in the main directory.

## Function Descriptions

### Main.py

This function is remarkably straightforward, orchestrating the timing of subfunction calls. Specifically, it oversees the execution of `projekty.py`, which is responsible for the comprehensive process of project dispatch. The original `main.py` module encompasses several other subfunctions, each delegated with distinct responsibilities such as SMS transmission.

### Mailing.py

The `mailing.py` module houses two pivotal functions dedicated to email transmission. One of these functions facilitates email attachments, while the other handles basic email dispatch. Notably, these functions return `True` as confirmation, allowing the designer to ascertain successful message delivery.

### Monday.py

The comprehensive management of the Monday platform is encapsulated within the `monday.py` module, spanning functions for extracting board lists, and editing specific items. Detailed explanations for each function can be found in comments preceding the respective function code.

### Projekty.py

At the core of the system, `projekty.py` presides, encompassing the holistic process management. The pivotal `tablify_process` function efficiently governs the database, promptly identifying deviations from expected outcomes. Upon detection of such discrepancies, the program adeptly captures errors and seamlessly proceeds to log them both in the CRM and within designated text files.

The ensuing subfunction, `download_data_from_monday`, meticulously retrieves client-centric data from the CRM. This dataset encompasses vital information such as client IDs, names, sales representatives (essential for `get_seller_email` to incorporate the seller in the email message), and email addresses.

These subordinate functions are invoked exclusively after loading the email message template, ingeniously designed in HTML format. Subsequently, the `find_items_by_column_values` function is activated, effectively pinpointing all projects slated for dispatch. Thereafter, the program meticulously iterates through each identified client, diligently extracting relevant data from the CRM, including the seller's email and the project information from Tablify.

Should any required columns contain empty fields, the program promptly generates an error message along the lines of: "Projekt nie wysłany - problem z Monday (sprawdź czy wymagane kolumny są uzupełnione[ID Montażu, Email])" (Project not sent - Monday-related issue, ensure mandatory columns are populated [Installation ID, Email]). Within the `data` variable, attributes like package details and remarks are seamlessly amalgamated, providing content for the email. Utilizing the `substitute` function, these variables are effectively merged into the email template, with the subject aptly set.

Consequently, the program triggers the email dispatch function. Upon successful transmission, the program promptly updates the CRM column to "Wysłany" (Sent), along with generating a corresponding CRM update to denote the project's successful dispatch.

In summation, the entire process meticulously orchestrates data retrieval, validation, email transmission, error management, and CRM updates for each project designated for delivery.