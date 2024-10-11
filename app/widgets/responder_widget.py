from kivy.uix.widget import Widget
from app import Responder


class ResponderWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.responder = Responder()

    def respond(self, text):
        return self.responder.respond(text)