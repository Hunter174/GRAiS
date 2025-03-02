from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import threading
import datetime
import os
from app.widgets.base_widget import BaseWidget

class GoogleWidget(BaseWidget):
    def __init__(self, **kwargs):
        super(GoogleWidget, self).__init__(**kwargs)

        # Layout configuration
        self.layout = BoxLayout(orientation='vertical', size_hint=(1, 1), height=200, spacing=1)

        # Corrected label with proper alignment
        self.label = Label(
            text="Initializing...",
            size_hint=(1, 1),
            size=(100, 100),  # Set size as needed
            halign="center",  # Center the text horizontally
            valign="middle",  # Center the text vertically
        )

        # Add the label to the layout
        self.layout.add_widget(self.label)

        # Add layout to the widget
        self.add_widget(self.layout)

        # Initialize Google API credentials in a separate thread
        self.creds = None
        threading.Thread(target=self._initialize_creds, daemon=True).start()

    def _initialize_creds(self):
        """Handles OAuth2.0 Authorization and initializes credentials."""
        scopes = ['https://www.googleapis.com/auth/calendar.readonly']
        credentials_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'credentials.json')
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes=scopes)
        try:
            self.creds = flow.run_local_server(port=8080)
        except Exception as e:
            print("Failed to complete OAuth process:", e)
        Clock.schedule_once(self._post_authorization)

    def _post_authorization(self, dt):
        """Fetches calendar events for the current week and updates the UI."""
        self.label.text = 'Fetching events for this week...'
        events = self.get_current_week_events()
        if events:
            self.display_events(events)
        else:
            self.label.text = 'No events found for this week.'

    def get_current_week_events(self):
        """Fetches upcoming events from Google Calendar for the current week."""
        service = build('calendar', 'v3', credentials=self.creds)
        today = datetime.datetime.utcnow()
        start_of_week = today - datetime.timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + datetime.timedelta(days=6)  # Sunday
        time_min = start_of_week.isoformat() + 'Z'
        time_max = end_of_week.isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=time_min,
                                              timeMax=time_max, singleEvents=True,
                                              orderBy='startTime').execute()
        return events_result.get('items', [])

    def display_events(self, events):
        """Formats and displays events in the UI."""
        formatted_events = []
        today = datetime.datetime.utcnow().date()

        for event in events:
            event_date = datetime.datetime.fromisoformat(
                event['start'].get('dateTime', event['start'].get('date')).rstrip('Z'))
            date = event_date.date()
            event_start_time = event_date.strftime('%H:%M')
            day_of_week = event_date.strftime('%A')
            month_day = event_date.strftime('%B %d')

            if date == today:
                formatted_events.append(f"{day_of_week}, {month_day} (Today):")
                summary = event['summary']
                formatted_events.append(f"  {event_start_time} - {summary}")

        if len(formatted_events) == 0:
            self.label.text = f"Nothing Scheduled for Today: {day_of_week}, {month_day}"

        else:
            self.label.text = '\n'.join(formatted_events)