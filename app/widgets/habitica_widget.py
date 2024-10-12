from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import threading
from app.logic.habitica_api import HabiticaAPI

class HabiticaWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(HabiticaWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Initialize the Habitica API
        self.habitica_api = HabiticaAPI()

        # Layout for player summary and todos
        self.player_info_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4), padding=10, spacing=10)
        self.todos_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4), padding=10, spacing=10)

        # Scroll view to display the player's summary
        self.summary_scroll_view = ScrollView(size_hint=(1, 0.5))
        self.summary_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.summary_layout.bind(minimum_height=self.summary_layout.setter('height'))
        self.summary_layout.add_widget(Label(text="Player Summary", size_hint_y=None, height=40,
                                             halign='left', valign='middle', bold=True, font_size='20sp'))
        self.summary_scroll_view.add_widget(self.summary_layout)

        # Scroll view to display the list of todos
        self.todos_scroll_view = ScrollView(size_hint=(1, 0.5))
        self.todos_grid_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.todos_grid_layout.bind(minimum_height=self.todos_grid_layout.setter('height'))
        self.todos_scroll_view.add_widget(self.todos_grid_layout)

        # Add the layouts to the widget
        self.add_widget(self.summary_scroll_view)
        self.add_widget(self.todos_scroll_view)

        # Notification label at the bottom
        self.notification_label = Label(text="No Notifications", size_hint=(1, 0.1))
        self.add_widget(self.notification_label)

        # Automatically fetch player summary and todos after initialization
        self.fetch_player_summary_thread()
        self.fetch_todos_thread()

    def fetch_todos_thread(self):
        """Start a daemon thread to fetch todos from Habitica"""
        threading.Thread(target=self.fetch_todos, daemon=True).start()

    def fetch_todos(self):
        """Fetch todos in a background thread"""
        todos = self.habitica_api.get_tasks()

        # Once the API call is complete, update the UI using the main thread
        Clock.schedule_once(lambda dt: self.display_todos(todos))

    def display_todos(self, todos):
        """Display open Habitica todos in the UI"""
        self.todos_grid_layout.clear_widgets()  # Clear the current list of todos

        if todos:
            for todo in todos:
                todo_label = Label(text=todo['text'], size_hint_y=None, height=40, halign='left', valign='middle')
                todo_label.text_size = (self.width - 20, None)  # Set text size to enable alignment
                self.todos_grid_layout.add_widget(todo_label)
            self.notification_label.text = f"Fetched {len(todos)} todos."
        else:
            self.notification_label.text = "Failed to fetch todos or no open todos found."


    def fetch_player_summary_thread(self):
        """Start a daemon thread to fetch player summary"""
        threading.Thread(target=self.fetch_player_summary, daemon=True).start()

    def fetch_player_summary(self):
        """Fetch player summary in the background and update UI."""
        player_summary = self.habitica_api.get_player_summary()

        # Once fetched, display the summary on the main UI thread
        Clock.schedule_once(lambda dt: self.display_summary(player_summary))

    def display_summary(self, player_summary):
        """Display the player's username, health, gold, and level."""
        self.summary_layout.clear_widgets()  # Clear previous summary

        if player_summary:
            # Extract data from the player summary
            username = player_summary['profile']['name']
            health = player_summary['stats']['hp']
            gold = player_summary['stats']['gp']
            level = player_summary['stats']['lvl']

            # Display the extracted information with left alignment
            username_label = Label(text=f"Username: {username}", size_hint_y=None, height=40, halign='left', valign='middle')
            username_label.text_size = (self.width - 20, None)
            health_label = Label(text=f"Health: {health} HP", size_hint_y=None, height=40, halign='left', valign='middle')
            health_label.text_size = (self.width - 20, None)
            gold_label = Label(text=f"Gold: {gold:.2f} GP", size_hint_y=None, height=40, halign='left', valign='middle')
            gold_label.text_size = (self.width - 20, None)
            level_label = Label(text=f"Level: {level}", size_hint_y=None, height=40, halign='left', valign='middle')
            level_label.text_size = (self.width - 20, None)

            # Add the labels to the summary layout
            self.summary_layout.add_widget(username_label)
            self.summary_layout.add_widget(health_label)
            self.summary_layout.add_widget(gold_label)
            self.summary_layout.add_widget(level_label)
        else:
            fail_label = Label(text="Failed to fetch player summary.", size_hint_y=None, height=40, halign='left', valign='middle')
            fail_label.text_size = (self.width - 20, None)  # Enable halign
            self.summary_layout.add_widget(fail_label)
