import numpy as np
import pyaudio
import wave
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line, Color
from kivy.clock import Clock


class AudioVisualizerKivy(Widget):
    def __init__(self, source_type='file', file_path=None, chunk_size=1024 * 4, rate=44100, **kwargs):
        super().__init__(**kwargs)
        self.source_type = source_type
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.rate = rate
        self.wav_file = None
        self.stream = None
        self.pyaudio_instance = pyaudio.PyAudio()
        self.recording = False
        self.recording_stream = None

        # Initialize the data source
        self.initialize_source()

        # Schedule updates at 60 FPS
        self.update_event = Clock.schedule_interval(self.update_visualization, 1 / 60.0)

    def initialize_source(self):
        """Initialize the audio source based on the source type."""
        self.stop_stream()  # Stop any existing stream

        if self.source_type == 'file':
            if not self.file_path:
                raise ValueError("file_path must be provided for 'file' source type.")
            self.init_file_stream()
        elif self.source_type == 'mic':
            self.init_mic_stream()

    def init_file_stream(self):
        # Open the wav file
        self.wav_file = wave.open(self.file_path, 'rb')

        # Initialize pyaudio stream for playing the audio file
        self.stream = self.pyaudio_instance.open(
            format=self.pyaudio_instance.get_format_from_width(self.wav_file.getsampwidth()),
            channels=self.wav_file.getnchannels(),
            rate=self.wav_file.getframerate(),
            output=True
        )

    def init_mic_stream(self):
        # Initialize pyaudio stream for capturing microphone input
        self.stream = self.pyaudio_instance.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

    def start_recording(self, filename="recorded_audio.wav"):
        """Start recording the microphone stream to a .wav file."""
        if self.source_type == 'mic':
            self.recording = True
            self.recording_filename = filename
            self.recording_stream = wave.open(self.recording_filename, 'wb')
            self.recording_stream.setnchannels(1)
            self.recording_stream.setsampwidth(self.pyaudio_instance.get_sample_size(pyaudio.paInt16))
            self.recording_stream.setframerate(self.rate)
            print("Recording started...")

    def stop_recording(self):
        """Stop recording the microphone stream and save the file."""
        if self.recording:
            self.recording = False
            self.recording_stream.close()
            print(f"Recording stopped and saved as {self.recording_filename}")

    def read_file_data(self):
        data = self.wav_file.readframes(self.chunk_size)
        if len(data) == 0:
            Clock.unschedule(self.update_event)
            return np.zeros(self.chunk_size, dtype=np.int16)

        # Play the audio data through the PyAudio stream
        self.stream.write(data)

        # Convert to numpy array for visualization
        return np.frombuffer(data, dtype=np.int16)

    def read_mic_data(self):
        # Capture audio data from the microphone
        data = self.stream.read(self.chunk_size, exception_on_overflow=False)

        # If recording, write the data to the recording file
        if self.recording and self.recording_stream:
            self.recording_stream.writeframes(data)

        return np.frombuffer(data, dtype=np.int16)

    def update_visualization(self, dt):
        # Read and visualize data based on the source type
        if self.source_type == 'file':
            data_int = self.read_file_data()
        elif self.source_type == 'mic':
            data_int = self.read_mic_data()

        # Apply scaling factor and offset for visualization
        scaling_factor = 0.01  # Adjust this value to scale up or down
        offset = 128  # Adjust this value to center the waveform
        scaled_data = data_int * scaling_factor + offset
        data_clipped = np.clip(scaled_data, 0, 255)

        # Clear the previous waveform
        self.canvas.clear()

        # Draw the waveform
        with self.canvas:
            Color(0.3, 0.6, 1)
            points = []
            for i, value in enumerate(data_clipped):
                x = i / len(data_clipped) * self.width
                y = value / 255 * self.height
                points.extend([x, y])

            # Draw the waveform as a line
            Line(points=points, width=1.5)

    def switch_source(self, new_source_type, file_path=None):
        """Switch between 'file' and 'mic' sources."""
        self.source_type = new_source_type
        if file_path:
            self.file_path = file_path

        # Reinitialize the audio source
        self.initialize_source()

        # Reschedule the update event to ensure the visualization continues
        if not self.update_event.is_triggered:
            self.update_event = Clock.schedule_interval(self.update_visualization, 1 / 60.0)

    def stop_stream(self):
        """Stop and clean up the current stream."""
        if self.source_type == 'file' and self.wav_file:
            self.wav_file.close()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.recording:
            self.stop_recording()

    def on_stop(self):
        """Clean up resources when the app is stopped."""
        self.stop_stream()
        self.pyaudio_instance.terminate()


class AudioApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Create the visualizer widget with an initial source
        self.visualizer = AudioVisualizerKivy(source_type='file', file_path='test.wav')

        # Create a button to switch between mic and file
        self.switch_button = Button(text="Switch to Mic", size_hint=(1, 0.1))
        self.switch_button.bind(on_press=self.switch_source)

        # Create a button to start/stop recording
        self.record_button = Button(text="Start Recording", size_hint=(1, 0.1))
        self.record_button.bind(on_press=self.toggle_recording)

        # Add the visualizer and buttons to the layout
        layout.add_widget(self.visualizer)
        layout.add_widget(self.switch_button)
        layout.add_widget(self.record_button)

        return layout

    def switch_source(self, instance):
        """Switch between file and mic sources based on the current source."""
        if self.visualizer.source_type == 'file':
            self.visualizer.switch_source('mic')
            instance.text = "Switch to File"
        else:
            self.visualizer.switch_source('file', file_path='test.wav')
            instance.text = "Switch to Mic"

    def toggle_recording(self, instance):
        """Start or stop recording based on the current state."""
        if self.visualizer.recording:
            self.visualizer.stop_recording()
            instance.text = "Start Recording"
        else:
            self.visualizer.start_recording(filename="recorded_audio.wav")
            instance.text = "Stop Recording"


if __name__ == '__main__':
    AudioApp().run()
