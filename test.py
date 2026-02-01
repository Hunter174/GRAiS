from core.agent.models.bt7274 import BT7274Agent
from core.tools.registry import get_tools

tools = get_tools("system",)# "web", "external")
agent = BT7274Agent(tools=tools)

out = agent.run("Say something short and interesting as BT-7274.")
text = out.content

print("LLM output:", text)