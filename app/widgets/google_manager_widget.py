from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label


class GoogleWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(GoogleWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10  # Add padding around the layout
        self.spacing = 10  # Add spacing between widgets

        # Create a horizontal layout for the top buttons
        top_button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

        # Notification label at the top
        self.notification_label = Label(text="No Notifications", size_hint=(1, 0.1))
        self.add_widget(self.notification_label)

        self.record_button = Button(text="Press and Hold to Record")
        self.auth_button = Button(text="Authorize Google Account")
        top_button_layout.add_widget(self.record_button)
        top_button_layout.add_widget(self.auth_button)

        # Add the horizontal layout to the main layout
        self.add_widget(top_button_layout)

        # Email and event form layout
        form_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4), spacing=10)
        self.email_input = TextInput(hint_text="Enter recipient email", size_hint=(1, 0.2))
        self.subject_input = TextInput(hint_text="Enter subject", size_hint=(1, 0.2))
        self.message_input = TextInput(hint_text="Enter message", size_hint=(1, 0.5))

        form_layout.add_widget(self.email_input)
        form_layout.add_widget(self.subject_input)
        form_layout.add_widget(self.message_input)

        self.add_widget(form_layout)

        # Button layout for sending email and scheduling event
        bottom_button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        self.send_button = Button(text="Send Email")
        self.event_button = Button(text="Schedule Event")

        bottom_button_layout.add_widget(self.send_button)
        bottom_button_layout.add_widget(self.event_button)

        self.add_widget(bottom_button_layout)