from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import threading
from app.logic.habitica_api import HabiticaAPI
from app.widgets.base_widget import BaseWidget

class HabiticaWidget(BaseWidget):
    def __init__(self, **kwargs):
        super(HabiticaWidget, self).__init__(**kwargs)

        # Initialize Habitica API
        self.habitica_api = HabiticaAPI()

        self.outer_layout = BoxLayout(
            orientation="vertical",
            padding=[20, 100, 20, 20],
            spacing=10,
            size_hint=(1, 1)
        )

        # Notification label
        self.notification_label = Label(
            text="Fetching todos...",
            size_hint=(1, None),
            height=40,
            halign="center",
        )
        self.outer_layout.add_widget(self.notification_label)

        # Create scrollable layout for todos
        self.todos_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.todos_layout.bind(minimum_height=self.todos_layout.setter('height'))

        # ScrollView for todos
        self.todos_scroll_view = ScrollView(size_hint=(1, 1))
        self.todos_scroll_view.add_widget(self.todos_layout)

        self.outer_layout.add_widget(self.todos_scroll_view)

        self.add_widget(self.outer_layout)

        # Start background thread to fetch todos
        threading.Thread(target=self.fetch_todos, daemon=True).start()

    def fetch_todos(self):
        """Fetch todos from Habitica."""
        todos = self.habitica_api.get_tasks()
        Clock.schedule_once(lambda dt: self.display_todos(todos))

    def display_todos(self, todos):
        """Display todos in the UI."""
        self.todos_layout.clear_widgets()

        for todo in todos:
            label = Label(
                text=todo['text'],
                size_hint_y=None,
                height=40,
                valign="middle",
                halign="center"
            )
            self.todos_layout.add_widget(label)

        # Ensure GridLayout resizes dynamically
        self.todos_layout.height = sum(child.height for child in self.todos_layout.children)

        self.notification_label.text = f"Fetched {len(todos)} todos."