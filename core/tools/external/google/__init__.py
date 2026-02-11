from .gmail import list_unread_emails, send_email
from .gcal import get_upcoming_events, create_calendar_event

TOOLS = [
    # Gmail tools
    list_unread_emails,
    send_email,

    # Gcal tools
    get_upcoming_events,
    create_calendar_event
]
