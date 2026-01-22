from datetime import datetime
import wikipedia
from langchain.tools import tool


@tool
def get_current_time() -> str:
    """Return the current local time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def wikipedia_lookup(query: str) -> str:
    """Look up a topic on Wikipedia and return a short summary."""
    try:
        return wikipedia.summary(query, sentences=3, auto_suggest=False)
    except wikipedia.DisambiguationError as e:
        return f"Topic is ambiguous. Possible options: {e.options[:5]}"
    except wikipedia.PageError:
        return "No Wikipedia page found for that query."
    except Exception as e:
        return f"Wikipedia lookup failed: {e}"


# Tool registry (single source of truth)
TOOLS = {
    "get_current_time": get_current_time,
    "wikipedia_lookup": wikipedia_lookup,
}
