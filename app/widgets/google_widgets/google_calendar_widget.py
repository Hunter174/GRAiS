from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import threading
import datetime
import pytz
import os
from app.widgets.base_widget import BaseWidget

# Set the localization (hard coded for now)
MST = pytz.timezone('America/Denver')

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

        today = datetime.datetime.now(MST).date()
        start_of_week = datetime.datetime.combine(today - datetime.timedelta(days=today.weekday()),
                                                  datetime.datetime.min.time(), MST)
        end_of_week = datetime.datetime.combine(start_of_week.date() + datetime.timedelta(days=6),
                                                datetime.datetime.max.time(), MST)

        # Convert to UTC for API request
        start_of_week_utc = start_of_week.astimezone(pytz.utc).isoformat()
        end_of_week_utc = end_of_week.astimezone(pytz.utc).isoformat()

        # Debugging output
        print(f"Requesting events from {start_of_week_utc} to {end_of_week_utc}")

        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_of_week_utc,
            timeMax=end_of_week_utc,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        return events_result.get('items', [])

    def display_events(self, events):
        """Formats and displays events in the UI."""
        formatted_events = []
        today = datetime.datetime.now(MST).date()

        for event in events:
            event_datetime_utc = datetime.datetime.fromisoformat(
                event['start'].get('dateTime', event['start'].get('date')).replace('Z', '')
            ).replace(tzinfo=pytz.utc)

            event_date = event_datetime_utc.astimezone(MST)

            date = event_date.date()
            event_start_time = event_date.strftime('%H:%M')
            day_of_week = event_date.strftime('%A')
            month_day = event_date.strftime('%B %d')

            if date == today:
                formatted_events.append(f"{day_of_week}, {month_day} (Today):")
                summary = event['summary']
                formatted_events.append(f"  {event_start_time} - {summary}")

        if not formatted_events:
            self.label.text = f"Nothing Scheduled for Today: {today.strftime('%A')}, {today.strftime('%B %d')}"
        else:
            self.label.text = '\n'.join(formatted_events)