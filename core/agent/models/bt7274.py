from langchain_ollama import ChatOllama
from core.agent.grais import GraisAgent
from core.agent.models.personas.persona_compiler import PersonaCompiler

class BT7274Agent(GraisAgent):
    name = "BT-7274"
    description = "Calm, tactical, mission-oriented AI companion"

    def __init__(self, tools, streaming=False):
        persona = PersonaCompiler.load_persona("bt7274.persona.yaml")
        system_prompt = PersonaCompiler().compile_system_prompt(persona)

        llm = (
            ChatOllama(
                model="gpt-oss:20b-cloud",
                temperature=0,
            )
            .bind_tools(tools)
        )

        # IMPORTANT: pass system_prompt down
        self.system_prompt = system_prompt

        super().__init__(llm=llm, tools=tools, streaming=streaming)