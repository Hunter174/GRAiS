from langchain_ollama import ChatOllama
from core.agent.grais import GraisAgent
from langchain.messages import SystemMessage, HumanMessage

class BT7274Agent(GraisAgent):
    """
    Titanfall-inspired tactical assistant.
    """

    name = "BT-7274"
    description = "Calm, tactical, mission-oriented AI companion"

    system_prompt = """
You are BT-7274, a tactical AI companion.
You are calm, concise, and mission-focused.
You prioritize operational clarity and objective completion.
"""

    def __init__(self, tools, streaming=False):
        llm = ChatOllama(
            model="gpt-oss:20b-cloud",
            temperature=0,
        ).bind_tools(tools)

        super().__init__(llm=llm, tools=tools, streaming=streaming)

    def run(self, user_input: str):
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_input),
        ]
        return self.llm.invoke(messages)