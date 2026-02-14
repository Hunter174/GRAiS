from langchain_ollama import ChatOllama
from core.agent.grais import GraisAgent
from core.agent.models.personas.persona_compiler import PersonaCompiler


class DefaultGRAiS(GraisAgent):
    name = "GRAiS"
    description = "Calm, friendly, helpful AI companion"

    def __init__(self, tools=None, streaming=False, enable_tts=False):
        persona = PersonaCompiler.load_persona("default.yaml")

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