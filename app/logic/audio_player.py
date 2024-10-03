import pyaudio
import wave
import numpy as np
from kivy.clock import Clock

class AudioPlayer:
    def __init__(self, source_type='file', file_path=None, recording_filename=None, chunk_size=4096, rate=44100):
        self.source_type = source_type
        self.file_path = file_path
        self.recording_filename = recording_filename
        self.chunk_size = chunk_size
        self.rate = rate
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None
        self.wav_file = None
        self.recording_stream = None
        self.recording_event = None
        self.recording = False

        self.initialize_source()

    def initialize_source(self):
        """Initialize the audio source based on source type."""
        self.stop_stream()
        if self.source_type == 'file':
            self.init_file_stream()
        elif self.source_type == 'mic':
            self.init_mic_stream()

    def init_file_stream(self):
        """Initialize file stream for audio playback."""
        try:
            self.wav_file = wave.open(self.file_path, 'rb')
            self.stream = self.pyaudio_instance.open(
                format=self.pyaudio_instance.get_format_from_width(self.wav_file.getsampwidth()),
                channels=self.wav_file.getnchannels(),
                rate=self.wav_file.getframerate(),
                output=True
            )
        except Exception as e:
            print(f"Error initializing file stream: {e}")

    def init_mic_stream(self):
        """Initialize microphone stream for recording."""
        try:
            self.stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
        except Exception as e:
            print(f"Error initializing mic stream: {e}")

    def start_stream_safe(self):
        """Start the audio stream safely via Kivy's event loop."""
        Clock.schedule_once(lambda dt: self.start_stream())

    def stop_stream(self):
        """Stop any active stream."""
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        if self.wav_file:
            self.wav_file.close()

    def start_stream(self):
        """Start stream based on current source type."""
        self.initialize_source()

    def read_data(self):
        """Read data from the current source."""
        if self.source_type == 'file':
            return self.read_file_data()
        elif self.source_type == 'mic':
            return self.read_mic_data()

    def read_file_data(self):
        """Read and play data from the audio file."""
        try:
            data = self.wav_file.readframes(self.chunk_size)
            if len(data) == 0:  # End of file
                return np.zeros(self.chunk_size, dtype=np.int16)

            self.stream.write(data)
            return np.frombuffer(data, dtype=np.int16)
        except Exception as e:
            print(f"Error reading file data: {e}")
            return np.zeros(self.chunk_size, dtype=np.int16)

    def read_mic_data(self):
        """Read data from the microphone stream."""
        try:
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            if self.recording and self.recording_stream:
                self.recording_stream.writeframes(data)
            return np.frombuffer(data, dtype=np.int16)
        except Exception as e:
            print(f"Error reading mic data: {e}")
            return np.zeros(self.chunk_size, dtype=np.int16)

    def start_recording(self, filename=None):
        """Start recording from the microphone stream."""
        if filename:
            self.recording_filename = filename

        try:
            self.recording_stream = wave.open(self.recording_filename, 'wb')
            self.recording_stream.setnchannels(1)
            self.recording_stream.setsampwidth(self.pyaudio_instance.get_sample_size(pyaudio.paInt16))
            self.recording_stream.setframerate(self.rate)
            self.recording = True
            self.init_mic_stream()
            self.recording_event = Clock.schedule_interval(self.record_mic_data, 0)
        except Exception as e:
            print(f"Error starting recording: {e}")
            self.recording = False

    def record_mic_data(self, dt):
        """Continuously read and record microphone data."""
        if self.recording:
            try:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                self.recording_stream.writeframes(data)
            except Exception as e:
                print(f"Error recording mic data: {e}")

    def stop_recording(self):
        """Stop recording and close the output file."""
        self.recording = False
        if self.recording_stream:
            self.recording_stream.close()
            self.recording_stream = None
        Clock.unschedule(self.recording_event)

    def switch_source(self, new_source_type, file_path=None):
        """Switch between different audio sources."""
        self.stop_stream()
        self.source_type = new_source_type
        if new_source_type == 'file' and file_path:
            self.file_path = file_path
        self.initialize_source()

    def terminate(self):
        """Terminate the PyAudio instance."""
        self.stop_stream()
        self.pyaudio_instance.terminate()
