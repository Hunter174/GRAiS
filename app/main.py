from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
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

        # Initialize with Greeting
        self.visualizer.start_visualization()

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
        try:
            self.visualizer.start_recording(filename=self.recorded_file_path)
            instance.text = "Recording..."
        except Exception as e:
            print(f"Error starting recording: {e}")
            instance.text = "Error: Could not record"

    def stop_and_process_audio(self, instance):
        """Stop recording when the button is released and process the audio."""
        try:
            # Disable the button to prevent interruptions during TTS and visualization
            instance.disabled = True
            self.visualizer.stop_recording()
            instance.text = "Processing..."

            # Process the audio in a separate thread to avoid blocking the UI
            threading.Thread(target=self.process_audio, args=(instance,)).start()
        except Exception as e:
            print(f"Error stopping and processing audio: {e}")
            instance.text = "Error: Could not process audio"
            instance.disabled = False

    def process_audio(self, instance):
        try:
            # Disable the button to prevent interruptions during TTS and visualization
            instance.disabled = True
            instance.text = "Processing..."

            # Stop any audio input/output streams to avoid conflicts
            Clock.schedule_once(lambda dt: self.visualizer.stop_stream())

            # Convert recorded audio to text
            transcribed_text = self.wav_to_text_widget.convert()
            print(f"Transcribed Text: {transcribed_text}")

            # Use Responder to generate a response
            response = self.responder_widget.respond(transcribed_text)
            print(f"Generated Response: {response}")

            # Save TTS response to a wav file
            tts_audio_path = os.path.join(os.path.dirname(__file__), 'audio', 'TTS_RESPONSE.wav')

            # Save the response as a wav file using TTS
            self.tts_widget.convert_to_wave(response)

            # Switch the visualizer to play and visualize the TTS audio
            Clock.schedule_once(lambda dt: self.visualizer.play_and_visualize_audio(tts_audio_path))

            # After playback is finished, re-enable the button
            Clock.schedule_once(lambda dt: self.enable_button(instance), 5)  # Adjust timing based on TTS duration

        except Exception as e:
            print(f"Error in processing audio: {e}")
            instance.disabled = False

    def enable_button(self, instance):
        """Re-enable the button after TTS and visualization have completed."""
        instance.text = "Press and Hold to Record"
        instance.disabled = False

    def on_stop(self):
        """Clean up resources when the app is stopped."""
        try:
            self.visualizer.stop_stream()
            self.visualizer.terminate()  # Terminate PyAudio safely

            # Ensure pyttsx3 engine is cleaned up
            if hasattr(self.tts_widget, 'tts'):
                del self.tts_widget.tts
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == '__main__':
    app = AudioApp()
    app.run()
