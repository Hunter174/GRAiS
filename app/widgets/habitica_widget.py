import threading
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock  # To update UI from a thread
from app.logic.habitica_api import HabiticaAPI

class HabiticaWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(HabiticaWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Initialize the Habitica API
        self.habitica_api = HabiticaAPI()

        # Fetch and display Habitica todos button
        self.get_todos_button = Button(text="Fetch Habitica Todos", size_hint=(1, 0.1))
        self.get_todos_button.bind(on_press=self.fetch_todos_thread)
        self.add_widget(self.get_todos_button)

        # Create a ScrollView to display the list of todos
        self.scroll_view = ScrollView(size_hint=(1, 0.9))  # Adjust size to take most of the screen
        self.todos_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.todos_layout.bind(minimum_height=self.todos_layout.setter('height'))  # Adjust height of layout automatically
        self.scroll_view.add_widget(self.todos_layout)
        self.add_widget(self.scroll_view)

        # Notification label at the bottom
        self.notification_label = Label(text="No Notifications", size_hint=(1, 0.1))
        self.add_widget(self.notification_label)

    def fetch_todos_thread(self, instance):
        """Start a daemon thread to fetch todos from Habitica"""
        threading.Thread(target=self.fetch_todos, daemon=True).start()

    def fetch_todos(self):
        """Fetch todos in a background thread"""
        todos = self.habitica_api.get_tasks()

        # Once the API call is complete, update the UI using the main thread
        Clock.schedule_once(lambda dt: self.display_todos(todos))

    def display_todos(self, todos):
        """Display open Habitica todos in the UI"""
        self.todos_layout.clear_widgets()  # Clear the current list of todos

        if todos:
            for todo in todos:
                todo_label = Label(text=todo['text'], size_hint_y=None, height=40)
                self.todos_layout.add_widget(todo_label)
            self.notification_label.text = f"Fetched {len(todos)} todos."
        else:
            self.notification_label.text = "Failed to fetch todos or no open todos found."
