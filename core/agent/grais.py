from abc import ABC
from typing import Iterable, Optional, Any
from langchain.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage, trim_messages
from langchain_core.messages.base import BaseMessage
from core.tts.infer import TextToSpeech
import logging

logger = logging.getLogger(__name__)


class GraisAgent(ABC):
    """
    Core agent abstraction.
    """

    name: str = "base"
    description: str = ""

    def __init__(self, llm: Any, system_prompt: str, tts_model_id: Optional[str] = None,
                tools: Optional[Iterable[Any]] = None, streaming: bool = False, enable_tts: bool = False):

        self.llm = llm
        self.system_prompt = system_prompt
        self.tools = list(tools) if tools else []
        self.streaming = streaming
        self.tts = TextToSpeech(tts_model_id) if (enable_tts and tts_model_id) else None

    def run(self, user_input: str, history: list[dict] | None = None):
        # Initialize messages with the system prompt first
        messages: list[BaseMessage] = [SystemMessage(content=self.system_prompt)]

        # Initialize the history container
        history_messages: list[BaseMessage] = []
        if history:
            for m in history:
                if m["role"] == "user":
                    history_messages.append(
                        HumanMessage(content=m["content"])
                    )
                elif m["role"] == "assistant":
                    history_messages.append(AIMessage(content=m["content"]))

            history_messages = trim_messages(history_messages, max_tokens=8000, token_counter="approximate")
            messages.extend(history_messages)

        # Add the users message at the end
        messages.append(HumanMessage(content=user_input))

        # Call the llm
        response = self.llm.invoke(messages)

        # Given the response decide on an action
        if isinstance(response, AIMessage) and response.tool_calls:
            tool_map = {tool.name: tool for tool in self.tools}
            tool_messages = []

            for call in response.tool_calls:
                tool = tool_map[call["name"]]
                result = tool.invoke(call["args"])

                logger.debug("Tool call: %s", tool.name)
                logger.debug("Result: %s", result)

                tool_messages.append(
                    ToolMessage(
                        tool_call_id=call["id"],
                        content=str(result),
                    )
                )

            messages.extend([response, *tool_messages])
            response = self.llm.invoke(messages)

        # TTS (only if configured)
        if self.tts and isinstance(response, AIMessage):
            self.tts.speak(response.content)

        return response