import speech_recognition as sr


class WavToText:
    def __init__(self, wav_file):
        self.wav_file = wav_file
        self.recognizer = sr.Recognizer()

    def convert_to_text(self):
        # Load the .wav file
        try:
            with sr.AudioFile(self.wav_file) as source:
                audio_data = self.recognizer.record(source)
                # Convert speech to text using Google's Speech Recognition API
                text = self.recognizer.recognize_google(audio_data)
                return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"
        except FileNotFoundError:
            return "File not found, please ensure the file path is correct."


# Example usage
if __name__ == "__main__":
    # Example .wav file, change this to the actual file path
    wav_to_text = WavToText("recorded_audio.wav")

    # Convert and print the text
    text_output = wav_to_text.convert_to_text()
    print(f"Transcribed Text: {text_output}")
