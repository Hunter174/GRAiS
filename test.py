from core.agent.models.bt7274 import BT7274Agent
from core.tools.registry import get_tools

tools = get_tools("system", "web", "external")
agent = BT7274Agent(tools=tools)

out = agent.run("Okay I now need you to send a test email to hunter.paxton@mines.sdsmt.edu, make the subject and body something interesting")

print(out.content)