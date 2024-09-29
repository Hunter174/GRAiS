from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from app.widgets.audio_visualizer_widget import AudioVisualizerWidget
from app.widgets.responder_widget import ResponderWidget
from app.widgets.tts_widget import TTSWidget
from app.widgets.wav_to_text_widget import WavToTextWidget
import os
import threading

class AudioApp(App):
    def build(self):
        # Define the base directory for audio files
        audio_dir = os.path.join(os.path.dirname(__file__), 'audio')
        self.file_path = os.path.join(audio_dir, 'GRAiS_AUDIO.wav')
        self.recorded_file_path = os.path.join(audio_dir, 'USER_AUDIO.wav')

        layout = BoxLayout(orientation='vertical')

        # Instantiate the audio player and visualizer with proper file paths
        self.visualizer = AudioVisualizerWidget(file_path=self.file_path, recorded_file_path=self.recorded_file_path)

        # Instantiate Responder, TTS, and WavToText widgets
        self.responder_widget = ResponderWidget()
        self.tts_widget = TTSWidget()
        self.wav_to_text_widget = WavToTextWidget(file_path=self.recorded_file_path)

        # Create a button to start recording on press and stop on release
        self.record_button = Button(text="Press and Hold to Record", size_hint=(1, 0.1))
        self.record_button.bind(on_press=self.start_recording)
        self.record_button.bind(on_release=self.stop_and_process_audio)

        # Add widgets and buttons to the layout
        layout.add_widget(self.visualizer)
        layout.add_widget(self.record_button)

        return layout

    def start_recording(self, instance):
        """Start recording when the button is pressed."""
        self.visualizer.start_recording(filename=self.recorded_file_path)
        instance.text = "Recording..."

    def stop_and_process_audio(self, instance):
        """Stop recording when the button is released and process the audio."""
        self.visualizer.stop_recording()
        instance.text = "Press and Hold to Record"

        # Process the audio in a separate thread to avoid blocking the UI
        threading.Thread(target=self.process_audio).start()

    def process_audio(self):
        try:
            # Convert recorded audio to text
            transcribed_text = self.wav_to_text_widget.convert()
            print(f"Transcribed Text: {transcribed_text}")

            # Use Responder to generate a response
            response = self.responder_widget.respond(transcribed_text)
            print(f"Generated Response: {response}")

            # Use TTS to speak the response
            self.tts_widget.speak_text(response)
        except Exception as e:
            print(f"Error in processing audio: {e}")

    def on_stop(self):
        """Clean up resources when the app is stopped."""
        self.visualizer.stop_stream()
        self.visualizer.terminate()
        # Ensure pyttsx3 engine is cleaned up
        del self.tts_widget.tts

if __name__ == '__main__':
    app = AudioApp()
    app.run()
