from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from core.agent.models.bt7274 import BT7274Agent
from core.agent.utility import AgentState, state_from_session, state_to_session
from core.tools.registry import get_tools

TOOL_SETS = {
    "system": ["system"],
    "system_web": ["system", "web"],
    "full": ["system", "web", "external"],
}

PERSONAS = {
    "bt7274": BT7274Agent,
}

ALLOWED_SETTINGS = {
    "enable_tts": bool,
}

def home_page(request):
    return render(request, "chat/home.html")

def chat_page(request):
    """Render the chat UI"""
    return render(
        request,
        "chat/chat.html",
        {
            "personas": list(PERSONAS.keys()),
            "tool_sets": list(TOOL_SETS.keys()),
        },
    )

@csrf_exempt
def reset_chat(request):
    request.session.flush()
    return JsonResponse({"status": "ok"})

@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        payload = json.loads(request.body)

        message = payload.get("message", "").strip()
        persona_key = payload.get("persona", "bt7274")
        tool_key = payload.get("tools", "system")
        enable_tts = payload.get("enable_tts", False)

        if not isinstance(enable_tts, bool):
            return JsonResponse({"error": "enable_tts must be boolean"}, status=400)

        if not message:
            return JsonResponse({"error": "Empty message"}, status=400)

        if persona_key not in PERSONAS:
            return JsonResponse({"error": "Invalid persona"}, status=400)

        if tool_key not in TOOL_SETS:
            return JsonResponse({"error": "Invalid tool set"}, status=400)

        # --- Load or initialize state ---
        raw_state = request.session.get("agent_state")
        state = state_from_session(raw_state) if raw_state else None

        cfg = (persona_key, tool_key, enable_tts)

        if not state or (state.persona, state.tools, state.enable_tts) != cfg:
            state = AgentState(
                persona=persona_key,
                tools=tool_key,
                enable_tts=enable_tts,
            )

        # --- Rebuild agent ---
        tools = get_tools(*TOOL_SETS[tool_key])
        Agent = PERSONAS[persona_key]

        agent = Agent(
            tools=tools,
            enable_tts=enable_tts,
        )

        # --- Run current turn with memory ---
        out = agent.run(message, state.messages)

        # --- Update memory ---
        state.messages.append({"role": "user", "content": message})
        state.messages.append({"role": "assistant", "content": out.content})

        # --- Persist back to session ---
        request.session["agent_state"] = state_to_session(state)

        return JsonResponse({
            "response": out.content,
            "tts_enabled": enable_tts,
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)