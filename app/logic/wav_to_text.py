import speech_recognition as sr

class WavToText:
    def __init__(self, wav_file):
        self.wav_file = wav_file
        self.recognizer = sr.Recognizer()

    def convert_to_text(self):
        try:
            with sr.AudioFile(self.wav_file) as source:
                audio_data = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            return f"API error: {e}"
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

