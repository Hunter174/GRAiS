import io
import numpy as np
import torch
import soundfile as sf
import re
from transformers import (
    SpeechT5Processor,
    SpeechT5ForTextToSpeech,
    SpeechT5HifiGan,
)
from huggingface_hub import hf_hub_download
from num2words import num2words


class TextToSpeech:
    VOCODER_ID = "microsoft/speecht5_hifigan"
    SAMPLE_RATE = 16000

    def __init__(self, model_id: str, device: str = "cpu"):
        self.model_id = model_id
        self.device = torch.device(device)

        embed_path = hf_hub_download(
            repo_id=self.model_id,
            filename="embedding.npy",
        )
        self.speaker_embeddings = (
            torch.tensor(np.load(embed_path), dtype=torch.float32)
            .unsqueeze(0)
            .to(self.device)
        )

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
    def synthesize(self, text: str) -> bytes:
        text = self._normalize_text(text)

        chunks = split_sentences(text)

        audio_parts = []

        for chunk in chunks:
            inputs = self.processor(text=chunk, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            spectrogram = self.model.generate_speech(
                inputs["input_ids"],
                self.speaker_embeddings,
            )
            speech = self.vocoder(spectrogram)

            audio_parts.append(speech.squeeze().cpu())

        full_audio = torch.cat(audio_parts)

        buffer = io.BytesIO()
        sf.write(buffer, full_audio.numpy(), self.SAMPLE_RATE, format="WAV")
        buffer.seek(0)
        return buffer.read()

def split_sentences(text: str, max_chars=300):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = ""

    for s in sentences:
        if len(current) + len(s) <= max_chars:
            current += " " + s if current else s
        else:
            chunks.append(current)
            current = s

    if current:
        chunks.append(current)

    return chunks