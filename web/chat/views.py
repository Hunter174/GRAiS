from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from core.agent.models.bt7274 import BT7274Agent
from core.tools.registry import get_tools

TOOL_SETS = {
    "system": ["system"],
    "system_web": ["system", "web"],
    "full": ["system", "web", "external"],
}

PERSONAS = {
    "bt7274": BT7274Agent,
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
def chat_api(request):
    """Handle chat messages"""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        payload = json.loads(request.body)

        message = payload.get("message", "").strip()
        persona_key = payload.get("persona", "bt7274")
        tool_key = payload.get("tools", "system")

        if not message:
            return JsonResponse({"error": "Empty message"}, status=400)

        if persona_key not in PERSONAS:
            return JsonResponse({"error": "Invalid persona"}, status=400)

        if tool_key not in TOOL_SETS:
            return JsonResponse({"error": "Invalid tool set"}, status=400)

        # Resolve tools safely
        tools = get_tools(*TOOL_SETS[tool_key])

        # Instantiate agent explicitly per request
        Agent = PERSONAS[persona_key]
        agent = Agent(tools=tools)

        out = agent.run(message)

        return JsonResponse({"response": out.content})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)