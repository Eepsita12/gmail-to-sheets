import os
import logging

from gmail_service import get_gmail_service
from email_parser import parse_email
from sheets_service import append_to_sheet,retry
from config import LAST_PROCESSED_PATH
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def read_last_state():
    if not os.path.exists(LAST_PROCESSED_PATH):
        return 0, ""
    
    with open(LAST_PROCESSED_PATH, "r") as f:
        content=f.read().strip()
        
    if not content:
        return 0, ""
    
    ts,msg_id = content.split("|")
    return int(ts), msg_id


def write_last_state(timestamp,msg_id):
    with open(LAST_PROCESSED_PATH, "w") as f:
        f.write(f"{timestamp}|{msg_id}")


def main():
    gmail_service, creds =get_gmail_service()
    last_ts, last_id= read_last_state()

    logging.info("Fetching unread messages")
    results=gmail_service.users().messages().list(
        userId="me",
        labelIds=["INBOX","UNREAD"],
        maxResults=50
    ).execute()
    
    messages=results.get("messages",[])
    if not messages:
        logging.info("No new emails")
        return
    
    rows=[]
    newest_ts=last_ts
    newest_id=last_id
    
    logging.info("Processing messages")
    
    for msg in messages:
        full_msg=gmail_service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()
        
        msg_ts=int(full_msg["internalDate"])
        
        if msg_ts<last_ts:
            continue
        if msg_ts == last_ts and msg["id"] <= last_id:
            continue
        
        parsed= parse_email(full_msg)
        
        rows.append([
            parsed["from"],
            parsed["subject"],
            parsed["date"],
            parsed["content"]     
        ])
        
        if msg_ts > newest_ts or (msg_ts == newest_ts and msg["id"] > newest_id):
            newest_ts = msg_ts
            newest_id = msg["id"]
        
        retry(lambda: gmail_service.users().messages().modify(
            userId="me",
            id=msg["id"],
            body={
                "removeLabelIds":["UNREAD"]
            }
        ).execute())
        
    if rows:
        logging.info(f"Appending {len(rows)} new emails to Google Sheets")
        append_to_sheet(creds, rows)
        write_last_state(newest_ts, newest_id)
        logging.info("Append done successfully")
    else:
        logging.info("No new emails since last run")    

if __name__ == "__main__":
    main()