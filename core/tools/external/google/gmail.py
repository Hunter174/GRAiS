from langchain.tools import tool
from googleapiclient.discovery import build
from core.tools.external.google.auth import get_credentials
from core.tools.external.google.config import GoogleConfig

CONFIG = GoogleConfig("google.config.yaml")

@tool
def list_unread_emails(max_results: int = 5) -> str:
    """List unread Gmail messages with sender and subject."""
    creds = get_credentials(
        CONFIG.credentials_file,
        CONFIG.token_file,
        CONFIG.scopes["all"],
    )

    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(
        userId="me",
        labelIds=["UNREAD"],
        maxResults=max_results,
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        return "No unread emails."

    summaries = []
    for msg in messages:
        meta = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
        ).execute()

        headers = {
            h["name"]: h["value"]
            for h in meta["payload"]["headers"]
        }

        summaries.append(f"From: {headers.get('From')} | Subject: {headers.get('Subject')}")

    return "\n".join(summaries)
