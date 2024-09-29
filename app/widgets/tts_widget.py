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