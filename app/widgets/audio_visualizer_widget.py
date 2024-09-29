from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Line, Color
import numpy as np

class AudioVisualizerWidget(Widget):
    def __init__(self, audio_player, **kwargs):
        super().__init__(**kwargs)
        self.audio_player = audio_player
        self.update_event = Clock.schedule_interval(self.update_visualization, 1 / 60.0)

    def update_visualization(self, dt):
        data_int = None

        # Read and visualize data based on the source type
        if self.audio_player.source_type == 'file':
            data_int = self.audio_player.read_file_data()
        elif self.audio_player.source_type == 'mic':
            data_int = self.audio_player.read_mic_data()

        # Ensure data_int is not None or empty
        if data_int is None or len(data_int) == 0:
            return

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

    def switch_source(self):
        """Switch between file and mic sources based on the current source."""
        if self.audio_player.source_type == 'file':
            self.audio_player.switch_source('mic')
            return "Switch to File"
        else:
            self.audio_player.switch_source('file', file_path=self.audio_player.file_path)
            return "Switch to Mic"
