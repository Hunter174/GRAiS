import pyttsx3
from audio_player import AudioApp

class RealTimeTTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('voice', voices[1].id)

    def convert_to_wav(self, text, file_name='test.wav'):
        self.engine.save_to_file(text, file_name)
        self.engine.runAndWait()

if __name__ == "__main__":
    # Step 1: Convert text to a .wav file
    tts = RealTimeTTS()
    tts.convert_to_wav("This is a test for text to speech.", file_name='test.wav')

    # Step 2: Play and visualize the generated .wav file
    AudioApp().run()
