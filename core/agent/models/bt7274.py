from langchain_ollama import ChatOllama
from core.agent.grais import GraisAgent
from core.agent.models.personas.persona_compiler import PersonaCompiler


class BT7274Agent(GraisAgent):
    name = "BT-7274"
    description = "Calm, tactical, mission-oriented AI companion"

    def __init__(self, tools=None, streaming=False, enable_tts=False):
        persona = PersonaCompiler.load_persona("bt7274.persona.yaml")

        system_prompt = PersonaCompiler.compile_system_prompt(persona)
        tts_model_id = PersonaCompiler.get_tts_model_id(persona)

        llm = (
            ChatOllama(
                model="gpt-oss:20b-cloud",
                temperature=0,
            )
            .bind_tools(tools or [])
        )

        super().__init__(
            llm=llm,
            system_prompt=system_prompt,
            tts_model_id=tts_model_id,
            tools=tools,
            streaming=streaming,
            enable_tts=enable_tts,
        )