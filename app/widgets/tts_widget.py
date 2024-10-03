import os
from kivy.uix.widget import Widget
from app.logic.text_to_speech import RealTimeTTS
from kivy.clock import Clock


class TTSWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tts = RealTimeTTS()

    def speak_text(self, text):
        """Speak the given text on the main thread."""
        Clock.schedule_once(lambda dt: self.tts.say(text))

    def convert_to_wave(self, text):
        """Convert text to a wav file on the main thread and save to 'audio/TTS_RESPONSE.wav'."""
        # Dynamically construct the path to the audio folder and file
        audio_dir = os.path.join(os.path.dirname(__file__), '../audio')
        wav_file_path = os.path.join(audio_dir, 'TTS_RESPONSE.wav')

        # Ensure the directory exists
        os.makedirs(audio_dir, exist_ok=True)

        # Use pyttsx3 to convert text to wav and save it to the path
        Clock.schedule_once(lambda dt: self.tts.convert_to_wav(text, wav_file_path))
