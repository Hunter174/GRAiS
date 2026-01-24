from pathlib import Path
import subprocess
import uuid

class TTSClient:
    def __init__(self, output_dir="audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def speak(self, text: str) -> Path:
        output_file = self.output_dir / f"{uuid.uuid4()}.wav"

        # Placeholder: replace with GPT-SoVITS call later
        subprocess.run(
            [
                "python",
                "infer.py",
                "--text",
                text,
                "--output",
                str(output_file),
            ],
            check=True,
        )

        return output_file
