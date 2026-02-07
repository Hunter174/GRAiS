from core.agent.models.bt7274 import BT7274Agent
from core.tools.registry import get_tools

tools = get_tools("system", "web", "external")
agent = BT7274Agent(tools=tools)

out = agent.run("I would like you to load my emails")
text = out.content

print("LLM output:", text)