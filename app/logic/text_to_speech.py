import pyttsx3

class RealTimeTTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('voice', self.engine.getProperty('voices')[0].id)
        self.is_processing = False  # Add a flag to check if the engine is busy

    def convert_to_wav(self, text, file_name):
        """Convert text to speech and save it to a wav file."""
        if not self.is_processing:
            self.is_processing = True
            self.engine.save_to_file(text, file_name)
            self.engine.runAndWait()  # Ensure the engine processes the entire text
            self.is_processing = False
        else:
            print("Engine is already processing a task. Please wait.")

    def say(self, text):
        if not self.is_processing:
            self.is_processing = True
            self.engine.say(text)
            self.engine.runAndWait()  # Ensure the engine processes the entire text
            self.is_processing = False
        else:
            print("Engine is already processing a task. Please wait.")
