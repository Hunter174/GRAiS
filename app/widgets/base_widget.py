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
            # Set the background color
            Color(1, 0.1, 0.1, 0.1)  # Light gray background (r, g, b, a)
            self.rect = Rectangle(size=self.size, pos=self.pos)

            # Add the gray outline
            Color(1, 0.5, 0.5, 1)  # Gray outline color
            self.outline = Line(rectangle=(*self.pos, *self.size), width=2)

        # Bind size and position to update the background and outline on resize
        self.bind(size=self._update_canvas, pos=self._update_canvas)

    def _update_canvas(self, *args):
        """Update the background rectangle and outline when resized or repositioned."""
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.outline.rectangle = (*self.pos, *self.size)

        # Ensure the background is updated properly on widget resize
        self.canvas.ask_update()