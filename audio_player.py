import numpy as np
import pyaudio
import wave
from kivy.app import App
from kivy.uix.widget import Widget
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

        # Initialize the data source based on the type
        if self.source_type == 'file':
            if not self.file_path:
                raise ValueError("file_path must be provided for 'file' source type.")
            self.init_file_stream()
        elif self.source_type == 'mic':
            self.init_mic_stream()

        # Schedule updates at 60 FPS
        Clock.schedule_interval(self.update_visualization, 1 / 60.0)

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

    def read_file_data(self):
        data = self.wav_file.readframes(self.chunk_size)
        if len(data) == 0:
            Clock.unschedule(self.update_visualization)
            return np.zeros(self.chunk_size, dtype=np.int16)

        # Play the audio data through the PyAudio stream
        self.stream.write(data)

        # Convert to numpy array for visualization
        return np.frombuffer(data, dtype=np.int16)

    def read_mic_data(self):
        # Capture audio data from the microphone
        data = self.stream.read(self.chunk_size, exception_on_overflow=False)
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

    def on_stop(self):
        # Clean up resources
        if self.source_type == 'file' and self.wav_file:
            self.wav_file.close()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.pyaudio_instance.terminate()

class AudioApp(App):
    def build(self):
        # You can choose either 'file' or 'mic' as the source type
        return AudioVisualizerKivy(source_type='mic')  # Switch to 'file' if you want to visualize from a file
