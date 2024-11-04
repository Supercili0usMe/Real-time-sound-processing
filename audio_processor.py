import pyaudio
import numpy as np

class AudioStream:
    def __init__(self):
        self.CHUNK = 1024 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.stream = None
        
    def start_stream(self, callback):
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=callback
        )
        self.stream.start_stream()
        
    def stop_stream(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

if __name__ == '__main__':
    # Проверка работы ввода и вывода аудио
    audio_stream = AudioStream()
    audio_stream.start_stream()
    audio_stream.stop_stream()

