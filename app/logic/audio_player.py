import pyaudio
import wave
import numpy as np
from kivy.clock import Clock


class AudioPlayer:
    def __init__(self, source_type='file', file_path=None, recording_filename=None, chunk_size=1024 * 4, rate=44100):
        self.source_type = source_type
        self.file_path = file_path
        self.recording_filename = recording_filename
        self.chunk_size = chunk_size
        self.rate = rate

        self.wav_file = None
        self.stream = None
        self.pyaudio_instance = pyaudio.PyAudio()
        self.recording = False
        self.recording_stream = None
        self.recording_event = None
        self.file_open = False

        self.initialize_source()

    def initialize_source(self):
        """Initialize the audio source based on the source type."""
        self.stop_stream()  # Ensure no stream is active before initializing a new one

        if self.source_type == 'file':
            if not self.file_path:
                raise ValueError("file_path must be provided for 'file' source type.")
            self.init_file_stream()
        elif self.source_type == 'mic':
            self.init_mic_stream()

    def init_file_stream(self):
        """Initialize the file stream for playback."""
        try:
            self.wav_file = wave.open(self.file_path, 'rb')
            self.stream = self.pyaudio_instance.open(
                format=self.pyaudio_instance.get_format_from_width(self.wav_file.getsampwidth()),
                channels=self.wav_file.getnchannels(),
                rate=self.wav_file.getframerate(),
                output=True
            )
            self.file_open = True
        except Exception as e:
            print(f"Failed to initialize file stream: {e}")
            self.file_open = False

    def init_mic_stream(self):
        """Initialize the microphone stream for recording."""
        try:
            self.stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
        except Exception as e:
            print(f"Failed to initialize mic stream: {e}")

    def start_stream_safe(self):
        """Safely start the audio stream within the Kivy event loop."""
        Clock.schedule_once(lambda dt: self.start_stream())

    def stop_stream_safe(self):
        """Safely stop the audio stream within the Kivy event loop."""
        Clock.schedule_once(lambda dt: self.stop_stream())

    def start_stream(self):
        """Start the audio stream."""
        if self.source_type == 'file':
            self.init_file_stream()
        elif self.source_type == 'mic':
            self.init_mic_stream()

    def stop_stream(self):
        """Stop and clean up the current stream."""
        if self.source_type == 'file' and self.wav_file:
            self.wav_file.close()
            self.file_open = False

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        if self.recording:
            self.stop_recording()

    def read_file_data(self):
        """Read data from the audio file in chunks."""
        if not self.file_open:
            print("Attempted to read from a closed file.")
            return np.zeros(self.chunk_size, dtype=np.int16)

        try:
            data = self.wav_file.readframes(self.chunk_size)
            if len(data) == 0:
                return np.zeros(self.chunk_size, dtype=np.int16)

            # Play the audio data through the PyAudio stream
            self.stream.write(data)

            # Convert to numpy array for visualization
            return np.frombuffer(data, dtype=np.int16)
        except Exception as e:
            print(f"Error reading file data: {e}")
            return np.zeros(self.chunk_size, dtype=np.int16)

    def read_mic_data(self):
        """Read data from the microphone stream."""
        try:
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)

            # If recording, write the data to the recording file
            if self.recording and self.recording_stream:
                self.recording_stream.writeframes(data)

            return np.frombuffer(data, dtype=np.int16)
        except Exception as e:
            print(f"Error reading mic data: {e}")
            return np.zeros(self.chunk_size, dtype=np.int16)

    def start_recording(self, filename=None):
        """Start recording the microphone stream to a .wav file."""
        if self.source_type != 'mic':
            raise ValueError("Recording can only be done with microphone as the source.")

        self.recording = True
        if filename:
            self.recording_filename = filename

        try:
            self.recording_stream = wave.open(self.recording_filename, 'wb')
            self.recording_stream.setnchannels(1)
            self.recording_stream.setsampwidth(self.pyaudio_instance.get_sample_size(pyaudio.paInt16))
            self.recording_stream.setframerate(self.rate)
            print(f"Recording started... Saving to {self.recording_filename}")

            # Open the microphone stream and start recording
            self.init_mic_stream()

            # Schedule continuous data capture while recording
            self.recording_event = Clock.schedule_interval(self.record_mic_data, 0)
        except Exception as e:
            print(f"Failed to start recording: {e}")
            self.recording = False

    def record_mic_data(self, dt):
        """Continuously read data from the microphone and save it while recording."""
        if self.recording:
            try:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                if self.recording_stream:
                    self.recording_stream.writeframes(data)
            except Exception as e:
                print(f"Error capturing audio: {e}")

    def stop_recording(self):
        """Stop recording the microphone stream and save the file."""
        if self.recording:
            self.recording = False
            if self.recording_stream:
                self.recording_stream.close()
            print(f"Recording stopped and saved as {self.recording_filename}")

    def switch_source(self, new_source_type, file_path=None):
        """Switch between 'file' and 'mic' sources."""
        self.stop_stream()  # Stop the current stream before switching
        self.source_type = new_source_type
        if new_source_type == 'file' and file_path:
            self.file_path = file_path
        self.initialize_source()  # Initialize the new source after stopping the previous stream

    def terminate(self):
        """Terminate the PyAudio instance."""
        self.stop_stream()  # Ensure any ongoing stream is stopped before termination
        self.pyaudio_instance.terminate()
