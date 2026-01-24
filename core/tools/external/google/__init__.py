from .gmail import list_unread_emails
from .gcal import get_upcoming_events

TOOLS = [
    list_unread_emails,
    get_upcoming_events,
]
