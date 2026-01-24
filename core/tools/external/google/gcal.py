from langchain.tools import tool
from googleapiclient.discovery import build
from datetime import datetime, timezone
from core.tools.external.google.auth import get_credentials
from core.tools.external.google.config import GoogleConfig

CONFIG = GoogleConfig("google.config.yaml")

@tool
def get_upcoming_events(max_results: int = 5) -> str:
    """Retrieve upcoming Google Calendar events."""
    creds = get_credentials(
        CONFIG.credentials_file,
        CONFIG.token_file,
        CONFIG.scopes["calendar"],
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

@tool
def create_calendar_event(title: str, start_iso: str, end_iso: str, description: str = "",
                          location: str = "", timezone_str: str = "UTC",) -> str:
    """
    Create a Google Calendar event.

    Args:
        title: Event title / summary
        start_iso: ISO-8601 datetime (e.g. 2026-01-25T14:00:00)
        end_iso: ISO-8601 datetime (e.g. 2026-01-25T15:00:00)
        description: Optional description
        location: Optional location
        timezone_str: Timezone (default UTC, e.g. America/Los_Angeles)
    """
    creds = get_credentials(
        CONFIG.credentials_file,
        CONFIG.token_file,
        CONFIG.scopes["calendar"],
    )

    service = build("calendar", "v3", credentials=creds)

    event_body = {
        "summary": title,
        "description": description,
        "location": location,
        "start": {
            "dateTime": start_iso,
            "timeZone": timezone_str,
        },
        "end": {
            "dateTime": end_iso,
            "timeZone": timezone_str,
        },
    }

    event = (
        service.events()
        .insert(calendarId="primary", body=event_body)
        .execute()
    )

    start = event["start"].get("dateTime", event["start"].get("date"))
    return f"Event created: {event['summary']} @ {start}"

# if __name__ == "__main__":
#     print(
#         create_calendar_event(
#             title="GRAiS Architecture Review",
#             start_iso="2026-01-25T14:00:00",
#             end_iso="2026-01-25T15:00:00",
#             description="Manual test event",
#             timezone_str="America/Los_Angeles",
#         )
#     )
