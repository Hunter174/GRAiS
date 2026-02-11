from langchain.tools import tool
from datetime import datetime

@tool
def get_current_time() -> str:
    """Return the current local time."""
    return datetime.now().isoformat()

TOOLS = [get_current_time]
