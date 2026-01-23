from langchain.tools import tool
from googleapiclient.discovery import build
from datetime import datetime, timezone

from .auth import get_credentials
from .config import GoogleConfig

CONFIG = GoogleConfig("google.config.yaml")

@tool
def get_upcoming_events(max_results: int = 5) -> str:
    """Retrieve upcoming Google Calendar events."""
    creds = get_credentials(
        CONFIG.credentials_file,
        CONFIG.token_file,
        CONFIG.scopes["all"],
    )

    service = build("calendar", "v3", credentials=creds)

    now = datetime.now(timezone.utc).isoformat()

    events = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute().get("items", [])

    if not events:
        return "No upcoming events."

    return "\n".join(
        f"{e['start'].get('dateTime', e['start'].get('date'))} — {e['summary']}"
        for e in events
    )
