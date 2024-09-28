from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from audio_player import AudioVisualizerKivy
from tts import RealTimeTTS
from app.wav_to_text import WavToText
from app.responder import Responder

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Initialize components
        self.visualizer = AudioVisualizerKivy(source_type='mic')
        self.tts = RealTimeTTS()
        self.responder = Responder()

        # Button to start/stop recording
        self.record_button = Button(text="Start Recording", size_hint=(1, 0.1))
        self.record_button.bind(on_press=self.toggle_recording)

        # Add widgets to the layout
        layout.add_widget(self.visualizer)
        layout.add_widget(self.record_button)

        return layout

    def toggle_recording(self, instance):
        if self.visualizer.recording:
            self.visualizer.stop_recording()
            instance.text = "Start Recording"

            # Convert recorded audio to text
            wav_to_text = WavToText("recorded_audio.wav")
            transcribed_text = wav_to_text.convert_to_text()
            print(f"Transcribed Text: {transcribed_text}")

            # Use Responder to generate a response
            response = self.responder.respond(transcribed_text)

            # Convert response to speech and play it
            self.tts.say(str(response))
            self.tts.engine.runAndWait()  # Ensure the TTS engine processes the speech
        else:
            self.visualizer.start_recording("recorded_audio.wav")
            instance.text = "Stop Recording"


if __name__ == '__main__':
    MainApp().run()
