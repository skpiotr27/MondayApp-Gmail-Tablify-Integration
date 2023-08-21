from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

flow = InstalledAppFlow.from_client_secrets_file('download_data/credentials.json', SCOPES)
credentials = flow.run_local_server()

print(f"Refresh Token: {credentials.refresh_token}")
