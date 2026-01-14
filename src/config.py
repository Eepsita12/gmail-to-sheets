import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATE_DIR = os.path.join(BASE_DIR, "state")

TOKEN_PATH = os.path.join(STATE_DIR, "token.json")

LAST_PROCESSED_PATH = os.path.join(STATE_DIR, "last_processed.txt")

CREDENTIALS_PATH = os.path.join(
    BASE_DIR, "credentials", "credentials.json"
)

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets"
]

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME", "Sheet1")
