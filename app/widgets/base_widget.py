from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line

class BaseWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(BaseWidget, self).__init__(**kwargs)
        self.orientation = "vertical"
        self._initialize_background()

    def _initialize_background(self):
        """Set the background color and add a gray outline."""
        with self.canvas.before:
            # Increase opacity for better visibility
            Color(1, 0.1, 0.1, 0.5)  # More visible light red background
            self.rect = Rectangle(size=self.size, pos=self.pos)

            # Add the gray outline
            Color(1, 0.5, 0.5, 1)  # Gray outline color
            self.outline = Line(rectangle=(*self.pos, *self.size), width=2)

        # Ensure the canvas updates when the widget resizes or moves
        self.bind(size=self._update_canvas, pos=self._update_canvas)

    def _update_canvas(self, *args):
        """Ensure background resizes correctly."""
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.outline.rectangle = (*self.pos, *self.size)
        self.canvas.ask_update()