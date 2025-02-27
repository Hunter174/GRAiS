from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window

# Import Necessary Logic
from app.widgets.utility_widgets.audio_visualizer_widget import AudioVisualizerWidget
from app.widgets.habitica_widgets.habitica_widget import HabiticaWidget
from app.widgets.google_widgets.google_calendar_widget import GoogleWidget

# Import the logic
from app.logic.responder import Responder
from app.logic.text_to_speech import RealTimeTTS
from app.logic.wav_to_text import WavToText

import os
import threading

class AudioApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Define the base directory for audio files
        audio_dir = os.path.join(os.path.dirname(__file__), 'audio')
        self.file_path = os.path.join(audio_dir, 'GRAiS_AUDIO.wav')
        self.recorded_file_path = os.path.join(audio_dir, 'USER_AUDIO.wav')

        # Instantiate the audio player and visualizer with proper file paths
        self.visualizer = AudioVisualizerWidget(self.file_path, self.recorded_file_path)

        # Instantiate Widgets
        self.google_widget = GoogleWidget()
        self.habitica_widget = HabiticaWidget()

        # Initiate Logic utility
        self.responder = Responder()
        self.tts = RealTimeTTS()
        self.wav_to_text = WavToText(self.recorded_file_path)

        # Initialize with Greeting
        self.visualizer.start_visualization()

        # Create a button to start recording on press and stop on release
        self.record_button = Button(text="Press and Hold to Record", size_hint=(1, 0.1))
        self.record_button.bind(on_press=self.start_recording)
        self.record_button.bind(on_release=self.stop_and_process_audio)

        # Bind the application quit event to handle cleanup
        Window.bind(on_request_close=self.quit_app)

    def build(self):
        layout = BoxLayout(orientation='vertical')
        visualizer_container = GridLayout(cols=1)
        information_container = GridLayout(cols=2)

        # Add to the visualizer widget
        visualizer_container.add_widget(self.visualizer)
        visualizer_container.add_widget(self.record_button)

        # Add to the summary info container
        information_container.add_widget(self.google_widget)
        information_container.add_widget(self.habitica_widget)

        # Add widgets and buttons to the layout
        layout.add_widget(information_container)
        layout.add_widget(visualizer_container)

        return layout

    def start_recording(self, instance):
        """Start recording when the button is pressed."""
        try:
            self.visualizer.start_recording(filename=self.recorded_file_path)
            instance.text = "Recording..."
        except Exception as e:
            print(f"Error starting recording: {e}")
            instance.text = "Error: Could not record"

    def stop_and_process_audio(self, instance):
        """Stop recording when the button is released and process the audio."""
        try:
            instance.disabled = True
            self.visualizer.stop_recording()
            instance.text = "Processing..."

            # Process the audio in a separate daemon thread to avoid blocking the UI
            thread = threading.Thread(target=self.process_audio, args=(instance,))
            thread.start()
            thread.join()

        except Exception as e:
            print(f"Error stopping and processing audio: {e}")
            instance.text = "Error: Could not process audio"
            instance.disabled = False

    def process_audio(self, instance):
        try:
            Clock.schedule_once(lambda dt: self.visualizer.stop_stream())

            transcribed_text = self.wav_to_text.convert_to_text()

            if transcribed_text is None:
                transcribed_text = ("Audio to Text processing error. Please respond to this message"
                                    "Telling me that the audio to text processing failed.")

            print(f"Transcribed Text: {transcribed_text}")

            response = self.responder.respond(transcribed_text)
            print(f"Generated Response: {response}")

            tts_audio_path = os.path.join(os.path.dirname(__file__), 'audio', 'TTS_RESPONSE.wav')
            self.tts.convert_to_wave(response)

            Clock.schedule_once(lambda dt: self.visualizer.play_and_visualize_audio(tts_audio_path))

            Clock.schedule_once(lambda dt: self.enable_button(instance), 5)

        except Exception as e:
            print(f"Error in processing audio: {e}")
            instance.disabled = False

    def enable_button(self, instance):
        """Re-enable the button after TTS and visualization have completed."""
        instance.text = "Press and Hold to Record"
        instance.disabled = False

    def quit_app(self, *args):
        """Handles app closing via the window's X button or programmatically."""
        print("Closing application...")

        try:
            if hasattr(self.visualizer, "stop_stream"):
                self.visualizer.stop_stream()

            if hasattr(self.visualizer, "terminate"):
                self.visualizer.terminate()

            if hasattr(self.google_widget, "creds") and self.google_widget.creds is not None:
                self.google_widget.creds = None

            if hasattr(self, "tts"):
                del self.tts

            print("Cleanup complete. Exiting application.")

        except Exception as e:
            print(f"Cleanup failed: {e}")

        return False

if __name__ == '__main__':
    try:
        app = AudioApp()
        app.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting gracefully.")
    finally:
        print("Cleanup finished. Goodbye!")