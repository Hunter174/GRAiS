from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class AgentState:
    persona: str
    tools: str
    enable_tts: bool
    messages: List[Dict] = field(default_factory=list)

def state_from_session(data: dict) -> AgentState:
    return AgentState(
        persona=data["persona"],
        tools=data["tools"],
        enable_tts=data["enable_tts"],
        messages=data.get("messages", []),
    )

def state_to_session(state: AgentState) -> dict:
    return {
        "persona": state.persona,
        "tools": state.tools,
        "enable_tts": state.enable_tts,
        "messages": state.messages,
    }
