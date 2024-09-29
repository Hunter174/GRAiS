import pyttsx3

class RealTimeTTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('voice', self.engine.getProperty('voices')[0].id)

    def convert_to_wav(self, text, file_name):
        self.engine.save_to_file(text, file_name)
        self.engine.runAndWait()

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()