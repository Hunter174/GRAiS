from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage, AIMessage
from logic.tools import TOOLS

llm = ChatOllama(
    model="gpt-oss:20b-cloud",
    temperature=0.1,
).bind_tools(list(TOOLS.values()))

def chat_once(user_input: str) -> str:
    messages = [HumanMessage(content=user_input)]

    while True:
        response = llm.invoke(messages)

        # Model requested tool(s)
        if isinstance(response, AIMessage) and response.tool_calls:
            messages.append(response)

            for call in response.tool_calls:
                tool_name = call["name"]
                tool_args = call.get("args", {})

                if tool_name not in TOOLS:
                    raise RuntimeError(f"Unknown tool requested: {tool_name}")

                tool_result = TOOLS[tool_name].invoke(tool_args)
                messages.append(AIMessage(content=tool_result, tool_call_id=call["id"],))

            # Let the model continue after tools
            continue

        # Final response (no more tools)
        return response.content

if __name__ == "__main__":
    print("Chat started. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        reply = chat_once(user_input)
        print(f"Assistant: {reply}\n")
