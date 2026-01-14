# Gmail to Google Sheets Automation (Python)

**Author:** Eepsita Modi

---

## Overview

This project is a Python-based automation system that reads real incoming emails from a Gmail account using the Gmail API, extracts relevant information, and appends the data into a Google Sheet using the Google Sheets API.

The script is designed to be idempotent and safe to re-run, ensuring:

* Only new emails are processed
* No duplicate rows are added
* Emails are marked as read after successful processing

The project uses **OAuth 2.0 (Desktop Application flow)** as required by the assignment.

---

## High-Level Architecture Diagram

![WhatsApp Image 2026-01-14 at 23 22 07](https://github.com/user-attachments/assets/9dd848c0-4e22-423d-87b3-66e1552bf8da)

---

## Video Demonstration

A short screen-recorded video demonstrating:
- Project flow
- Gmail → Google Sheets data movement
- Duplicate prevention logic
- Behavior when the script is run multiple times

📎 Video Link: https://drive.google.com/file/d/15ElnhBzoC9xZYlccfGfz492qdxRRMy0d/view?usp=sharing


## Project Structure

```
gmail-to-sheets/
├── credentials/
│   └── credentials.json        # OAuth client credentials (NOT committed)
├── src/
│   ├── main.py                 # Orchestration logic
│   ├── gmail_service.py        # Gmail OAuth & API setup
│   ├── sheets_service.py       # Google Sheets operations
│   ├── email_parser.py         # Email parsing & HTML cleanup
│   └── config.py               # Central configuration
├── state/
│   ├── token.json              # OAuth token (NOT committed)
│   └── last_processed.txt      # Persistent processing state (NOT committed)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Authentication (OAuth 2.0 Flow)

* Uses Google OAuth 2.0 Desktop Application flow
* On first run, a browser window opens for user consent
* OAuth access token is stored locally in `state/token.json`
* Subsequent runs reuse the stored token automatically

**Security:**
OAuth tokens and credentials are explicitly excluded from version control using `.gitignore`.

---

## Data Stored in Google Sheets

Each processed email is appended as a new row with the following columns:

```
From | Subject | Date | Content
```

* Headers are automatically created if the sheet is empty
* Email content is truncated to avoid excessively large cells
* Data is appended (never overwritten)

---

## State Management (Critical Requirement)

### Why state is required

Without state management:

* Emails would be reprocessed on every run
* Duplicate rows would be added to the Google Sheet

---

### How state is stored

State is stored locally in:

```
state/last_processed.txt
```

**Format:**

```
<timestamp>|<message_id>
```

Example:

```
1705209142000|18c7f2a1b4e3d912
```

* `timestamp` → Gmail `internalDate` (milliseconds)
* `message_id` → Unique Gmail message ID

---

### How state is used

Before processing each email:

* Emails older than the stored timestamp are skipped
* Emails with the same timestamp but lower or equal message IDs are skipped

This guarantees:

* No duplicate rows
* Correct handling of same-timestamp emails
* Safe re-execution of the script

---

## Duplicate Prevention Logic

Duplicate prevention is achieved using three layers:

1. Gmail query fetches unread emails only
2. Persistent state file prevents reprocessing old messages
3. Emails are marked as read only after successful append

This ensures idempotent behavior across multiple runs.

---

## Challenges Faced & Solution

### Challenge

Handling duplicate emails when the script is re-run, especially when multiple emails share the same timestamp.

### Solution

This was solved by implementing a persistent state mechanism that stores both the **timestamp** and **message ID** of the last processed email. This ensures precise ordering and prevents duplicates even in edge cases.

---

## Logging

The script uses structured logging in the format:

```
YYYY-MM-DD HH:MM:SS | LEVEL | Message
```

Examples:

* `Fetching unread messages`
* `Appending 3 new emails to Google Sheets`
* `No new emails since last run`

This improves debugging and traceability.

---

## Step-by-Step Setup Instructions

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add OAuth credentials

Place your Google OAuth client file at:

```
credentials/credentials.json
```

### Run the script

```bash
python src/main.py
```

---

## Limitations of the Solution

* Email attachments are not processed
* Inline images are ignored
* The script runs as a batch job, not a real-time service
* Designed for a single Gmail account

These limitations were intentional to keep the solution focused and aligned with the assignment scope.

---

## Conclusion

This project demonstrates:

* Correct usage of Gmail & Google Sheets APIs
* Secure OAuth 2.0 authentication
* Reliable state persistence
* Duplicate-safe, repeatable automation
* Clean, modular Python architecture



