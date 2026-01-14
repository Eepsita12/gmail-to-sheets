import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import (TOKEN_PATH, CREDENTIALS_PATH, SCOPES, STATE_DIR)

def get_gmail_service():
    creds= None

    os.makedirs(STATE_DIR,exist_ok=True)

    if os.path.exists(TOKEN_PATH):
        creds=Credentials.from_authorized_user_file(TOKEN_PATH,SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow= InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds=flow.run_local_server(port=0)
        
        with open(TOKEN_PATH,"w") as token:
            token.write(creds.to_json())

    gmail_service=build("gmail","v1", credentials=creds)
    return gmail_service, creds
