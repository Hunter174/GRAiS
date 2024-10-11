from app import AudioPlayer
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Line, Color
import numpy as np

class AudioVisualizerWidget(Widget):
    def __init__(self, file_path=None, recorded_file_path=None, **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.recorded_file_path = recorded_file_path
        self.audio_player = AudioPlayer(source_type='file', file_path=self.file_path, recording_filename=self.recorded_file_path)
        self.update_event = None

    def start_recording(self, filename=None):
        """Start recording through the AudioPlayer and begin visualization."""
        if filename:
            self.recorded_file_path = filename
        try:
            self.audio_player.switch_source('mic')
            self.audio_player.start_recording(self.recorded_file_path)
            self.start_visualization()
        except Exception as e:
            print(f"Error during recording start: {e}")
            self.stop_visualization()

    def stop_recording(self):
        """Stop recording and visualization."""
        self.audio_player.stop_recording()
        self.stop_visualization()

    def start_visualization(self):
        """Schedule visualization updates."""
        if self.update_event:  # Prevent multiple intervals from being scheduled
            self.stop_visualization()
        self.update_event = Clock.schedule_interval(self.update_visualization, 1 / 60.0)

    def stop_visualization(self):
        """Unschedule visualization updates."""
        if self.update_event:
            Clock.unschedule(self.update_event)
            self.update_event = None
        self.canvas.clear()  # Clear canvas when visualization stops

    def stop_stream(self):
        """Stop visualization and audio stream."""
        self.stop_visualization()
        self.audio_player.stop_stream()

    def update_visualization(self, dt):
        """Read audio data and update visualization."""
        data_int = self.audio_player.read_data()

        # Ensure data is valid
        if data_int is None or len(data_int) == 0:
            self.stop_stream()
            return

        # Scale and offset data for visualization
        scaling_factor = 0.01
        offset = 128
        scaled_data = data_int * scaling_factor + offset
        data_clipped = np.clip(scaled_data, 0, 255)

        # Clear canvas and draw waveform
        self.canvas.clear()
        with self.canvas:
            Color(0.3, 0.6, 1)
            points = [self.get_point(i, value, len(data_clipped)) for i, value in enumerate(data_clipped)]
            Line(points=sum(points, []), width=1.5)

    def get_point(self, i, value, data_length):
        """Helper method to calculate (x, y) coordinates for waveform points."""
        x = i / data_length * self.width
        y = value / 255 * self.height
        return [x, y]

    def switch_source(self):
        """Toggle between file and mic sources."""
        try:
            if self.audio_player.source_type == 'file':
                self.audio_player.switch_source('mic')
            else:
                self.audio_player.switch_source('file', file_path=self.audio_player.file_path)
        except Exception as e:
            print(f"Error switching source: {e}")

    def play_and_visualize_audio(self, wav_file_path):
        """Play and visualize a WAV file."""
        try:
            self.audio_player.switch_source('file', file_path=wav_file_path)
            self.audio_player.start_stream_safe()
            self.start_visualization()
        except Exception as e:
            print(f"Error during audio playback and visualization: {e}")

    def terminate(self):
        """Terminate the AudioPlayer instance."""
        try:
            self.audio_player.terminate()
        except Exception as e:
            print(f"Error terminating AudioPlayer: {e}")