from core.agent.models.bt7274 import BT7274Agent
from core.tools.registry import get_tools

tools = get_tools("system", "web")
agent = BT7274Agent(tools=tools)

out = agent.run("How are you supposed to act?")

print(out.content)