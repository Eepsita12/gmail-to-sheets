import base64
from bs4 import BeautifulSoup


def decode(data):
    return base64.urlsafe_b64decode(data).decode("utf-8", "ignore")


def extract_parts(payload):
    if "parts" not in payload:
        return [payload]

    parts = []
    for part in payload["parts"]:
        parts.extend(extract_parts(part))
    return parts


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def parse_email(message):
    payload = message["payload"]

    headers = payload.get("headers", [])
    header_map = {h["name"]: h["value"] for h in headers}

    body = ""
    parts = extract_parts(payload)
    for part in parts:
        if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
            body = decode(part["body"]["data"])
            break

    if not body:
        for part in parts:
            if part.get("mimeType") == "text/html" and part.get("body", {}).get("data"):
                html = decode(part["body"]["data"])
                body = clean_html(html)
                break

    body = body.strip()

    return {
        "from": header_map.get("From", ""),
        "subject": header_map.get("Subject", ""),
        "date": header_map.get("Date", ""),
        "content": clean_html(body) if "<" in body else body
    }
