import numpy as np
import torch
import soundfile as sf
import re
from pathlib import Path
from transformers import (
    SpeechT5Processor,
    SpeechT5ForTextToSpeech,
    SpeechT5HifiGan,
)
from huggingface_hub import hf_hub_download
from playsound3 import playsound
from num2words import num2words


class TextToSpeech:
    VOCODER_ID = "microsoft/speecht5_hifigan"
    SAMPLE_RATE = 16000

    def __init__(self, model_id: str, output_dir: str | Path = ".", device: str = "cpu"):
        self.model_id = model_id
        self.device = torch.device(device)

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Speaker embedding
        embed_path = hf_hub_download(
            repo_id=self.model_id,
            filename="embedding.npy",
        )
        self.speaker_embeddings = (
            torch.tensor(np.load(embed_path), dtype=torch.float32)
            .unsqueeze(0)
            .to(self.device)
        )

        # Model stack
        self.processor = SpeechT5Processor.from_pretrained(self.model_id)

        self.model = (
            SpeechT5ForTextToSpeech.from_pretrained(self.model_id)
            .to(self.device)
            .eval()
        )

        self.vocoder = (
            SpeechT5HifiGan.from_pretrained(self.VOCODER_ID)
            .to(self.device)
            .eval()
        )

    def _normalize_text(self, text: str) -> str:
        def percent_repl(match):
            return f"{num2words(match.group(1))} percent"

        text = re.sub(r"(\d+)%", percent_repl, text)
        text = re.sub(r"\b\d+\b", lambda m: num2words(m.group()), text)
        text = re.sub(r"[^\w\s\.,!?']", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @torch.no_grad()
    def generate_wav(self, text: str, filename: str = "tts.wav") -> Path:
        output_path = self.output_dir / filename

        inputs = self.processor(text=text, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        spectrogram = self.model.generate_speech(
            inputs["input_ids"],
            self.speaker_embeddings,
        )

        speech = self.vocoder(spectrogram)

        sf.write(
            output_path,
            speech.squeeze().cpu().numpy(),
            self.SAMPLE_RATE,
        )

        return output_path

    def speak(self, text: str, filename: str = "tts.wav") -> Path:
        normalized = self._normalize_text(text)
        wav_path = self.generate_wav(normalized, filename)
        playsound(str(wav_path))
        return wav_path