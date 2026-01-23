from abc import ABC, abstractmethod
from typing import Iterable, Optional, Any
from langchain.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

class GraisAgent(ABC):
    """
    Core agent abstraction.
    """

    name: str = "base"
    description: str = ""
    system_prompt: str = ""

    def __init__(
        self,
        llm: Any,
        tools: Optional[Iterable[Any]] = None,
        streaming: bool = False,
    ):
        self.llm = llm
        self.tools = list(tools) if tools else []
        self.streaming = streaming

    def run(self, user_input: str):
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_input),
        ]

        response = self.llm.invoke(messages)

        if isinstance(response, AIMessage) and response.tool_calls:
            tool_map = {tool.name: tool for tool in self.tools}

            tool_messages = []
            for call in response.tool_calls:
                tool = tool_map[call["name"]]
                result = tool.invoke(call["args"])

                tool_messages.append(
                    ToolMessage(
                        tool_call_id=call["id"],
                        content=str(result),
                    )
                )

            # Send tool output back to the LLM
            messages.extend([response, *tool_messages])
            return self.llm.invoke(messages)

        return response