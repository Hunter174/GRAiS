from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import threading
from app.logic.habitica_api import HabiticaAPI
from app.widgets.base_widget import BaseWidget

class HabiticaWidget(BaseWidget):
    def __init__(self, **kwargs):
        super(HabiticaWidget, self).__init__(**kwargs)

        # Initialize Habitica API
        self.habitica_api = HabiticaAPI()

        # Create scrollable layout for todos
        self.todos_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.todos_layout.bind(minimum_height=self.todos_layout.setter('height'))

        # ScrollView for todos
        self.todos_scroll_view = ScrollView(size_hint=(1, None), size=(200, 300))  # Set size_hint for ScrollView
        self.todos_scroll_view.add_widget(self.todos_layout)

        self.add_widget(self.todos_scroll_view)

        # Notification label
        self.notification_label = Label(text="Fetching todos...", size_hint=(1, None), height=40)
        self.notification_label.halign = "center"  # Center the text horizontally
        self.add_widget(self.notification_label)

        # Start background thread to fetch todos
        threading.Thread(target=self.fetch_todos, daemon=True).start()

    def fetch_todos(self):
        """Fetch todos."""
        todos = self.habitica_api.get_tasks()
        Clock.schedule_once(lambda dt: self.display_todos(todos))

    def display_todos(self, todos):
        """Display todos in the UI."""
        self.todos_layout.clear_widgets()
        for todo in todos:
            label = Label(text=todo['text'], size_hint_y=None, height=40)
            self.todos_layout.add_widget(label)
        self.notification_label.text = f"Fetched {len(todos)} todos."