from core.tools.system import TOOLS as SYSTEM_TOOLS
from core.tools.web import TOOLS as WEB_TOOLS
from core.tools.data import TOOLS as DATA_TOOLS
from core.tools.external import TOOLS as EXTERNAL_TOOLS
from core.tools.external.google import TOOLS as GOOGLE_TOOLS

ALL_TOOLS = (
    SYSTEM_TOOLS
    + WEB_TOOLS
    + DATA_TOOLS
    + EXTERNAL_TOOLS
    + GOOGLE_TOOLS
)

def get_tools(*groups: str):
    mapping = {
        "system": SYSTEM_TOOLS,
        "web": WEB_TOOLS,
        "data": DATA_TOOLS,
        "external": EXTERNAL_TOOLS,
    }

    tools = []
    for group in groups:
        tools.extend(mapping[group])

    return tools