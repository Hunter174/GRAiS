from pathlib import Path
import yaml

class PersonaCompiler:
    @staticmethod
    def load_persona(path: str) -> dict:
        base_dir = Path(__file__).resolve().parent
        persona_path = base_dir / path

        with open(persona_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def compile_system_prompt(persona: dict) -> str:
        lines = []

        # Identity (abstracted)
        lines.append(f"You are {persona['persona_name']}, a tactical AI assistant.")
        lines.append("")

        # Tone
        if "tone" in persona:
            lines.append("Tone:")
            for t in persona["tone"]:
                lines.append(f"- {t}")
            lines.append("")

        # Speech style
        if "speech_style" in persona:
            lines.append("Speech style:")
            for s in persona["speech_style"]:
                lines.append(f"- {s}")
            lines.append("")

        # Core protocols
        if "core_protocols" in persona:
            lines.append("Core protocols:")
            for i, p in enumerate(persona["core_protocols"], start=1):
                lines.append(f"{i}. {p}")
            lines.append("")

        # Behavioral rules
        if "behavioral_rules" in persona:
            lines.append("Behavioral rules:")
            for r in persona["behavioral_rules"]:
                lines.append(f"- {r}")
            lines.append("")

        # Tool policy
        if "tool_policy" in persona:
            lines.append("Tool usage policy:")
            for t in persona["tool_policy"]:
                lines.append(f"- {t}")
            lines.append("")

        # Style examples
        if "examples" in persona:
            lines.append("Style reference examples (do not quote verbatim unless appropriate):")
            for ex in persona["examples"]:
                # support both raw strings and structured examples
                if isinstance(ex, dict):
                    lines.append(f'- "{ex["text"]}"')
                else:
                    lines.append(f'- "{ex}"')
            lines.append("")

        return "\n".join(lines).strip()