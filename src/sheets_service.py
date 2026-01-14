import time
import logging

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from config import SCOPES

SPREADSHEET_ID="1_0JFhvSFr_aZg7XG8ydYNtALbD7BQPy1DwRm76CRdUI"
SHEET_NAME="Sheet1"
DATA_RANGE=f"{SHEET_NAME}!A:D"
HEADER_RANGE=f"{SHEET_NAME}!A1:D1"

def retry(operation, retries=3, delay=2):
    for attempt in range(1, retries+1):
        try:
            return operation()
        except Exception as e:
            logging.error(f"Attempt {attempt} failed: {e}")
            if attempt<retries:
                time.sleep(delay)
            else:
                raise
                     
def ensure_headers(service):
    result=service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=HEADER_RANGE,
    ).execute()
    
    values=result.get("values", [])
    
    if not values:
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=HEADER_RANGE, 
            valueInputOption="RAW",
            body = {
                "values": [[
                    "From",
                    "Subject",
                    "Date",
                    "Content"
                    
                ]]
            }
        ).execute()
        

def append_to_sheet(creds,rows):
    service=build("sheets","v4", credentials=creds)
    ensure_headers(service) 
    
    retry(lambda: service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=DATA_RANGE,
        valueInputOption="RAW",
        body={"values":rows}
    ).execute())