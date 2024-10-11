from kivy.uix.widget import Widget
from app import WavToText


class WavToTextWidget(Widget):
    def __init__(self, file_path, **kwargs):
        super().__init__(**kwargs)
        self.wav_to_text = WavToText(file_path)

    def convert(self):
        return self.wav_to_text.convert_to_text()