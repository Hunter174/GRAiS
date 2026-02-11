from abc import ABC
from typing import Iterable, Optional, Any
from langchain.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage, trim_messages
from core.tts.registry import get_tts
import logging

logger = logging.getLogger(__name__)


class GraisAgent(ABC):
    name: str = "base"
    description: str = ""

    def __init__(self, llm: Any, system_prompt: str, tts_model_id: Optional[str] = None,
                tools: Optional[Iterable[Any]] = None, streaming: bool = False, enable_tts: bool = False):

        self.llm = llm
        self.system_prompt = system_prompt
        self.tools = list(tools) if tools else []
        self.streaming = streaming
        self.tts = get_tts(tts_model_id) if (enable_tts and tts_model_id) else None

    def run(self, user_input: str, history: list[dict] | None = None):
        messages = [SystemMessage(content=self.system_prompt)]

        if history:
            for m in history:
                if m["role"] == "user":
                    messages.append(HumanMessage(content=m["content"]))
                elif m["role"] == "assistant":
                    messages.append(AIMessage(content=m["content"]))

            messages = trim_messages(messages, max_tokens=8000, token_counter="approximate")

        messages.append(HumanMessage(content=user_input))

        response = self.llm.invoke(messages)

        # Tool execution (unchanged)
        if isinstance(response, AIMessage) and response.tool_calls:
            tool_map = {tool.name: tool for tool in self.tools}
            tool_messages = []

            for call in response.tool_calls:
                result = tool_map[call["name"]].invoke(call["args"])
                tool_messages.append(
                    ToolMessage(
                        tool_call_id=call["id"],
                        content=str(result),
                    )
                )

            messages.extend([response, *tool_messages])
            response = self.llm.invoke(messages)

        audio_bytes = None
        if self.tts and isinstance(response, AIMessage):
            audio_bytes = self.tts.synthesize(response.content)

        return {
            "text": response.content,
            "audio": audio_bytes,
        }
