import pyttsx3
from kivy.clock import Clock
import os

class RealTimeTTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('voice', self.engine.getProperty('voices')[0].id)
        self.is_processing = False  # Add a flag to check if the engine is busy

    def convert_to_wave(self, text):
        """Convert text to a wav file on the main thread and save to 'audio/TTS_RESPONSE.wav'."""
        # Dynamically construct the path to the audio folder and file
        audio_dir = os.path.join(os.path.dirname(__file__), '../audio')
        wav_file_path = os.path.join(audio_dir, 'TTS_RESPONSE.wav')

        # Ensure the directory exists
        os.makedirs(audio_dir, exist_ok=True)

        # Use pyttsx3 to convert text to wav and save it to the path
        Clock.schedule_once(lambda dt: self.convert_to_wav(text, wav_file_path))


    def convert_to_wav(self, text, file_name):
        """Convert text to speech and save it to a wav file."""
        try:
            # Save text to the specified file
            self.engine.save_to_file(text, file_name)
            self.engine.runAndWait()  # Ensure the engine processes the entire text
            print(f"Successfully saved speech to {file_name}")
        except Exception as e:
            print(f"Error converting text to wav: {e}")

    def say(self, text):
        if not self.is_processing:
            self.is_processing = True
            self.engine.say(text)
            self.engine.runAndWait()  # Ensure the engine processes the entire text
            self.is_processing = False
        else:
            print("Engine is already processing a task. Please wait.")
