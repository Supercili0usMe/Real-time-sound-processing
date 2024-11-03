import time
import pyaudio
import numpy as np
import threading

class AudioStream:
    # Инициализируем класс базовыми переменными
    def __init__(self):
        self.CHUNK = 1024 * 2           # Размер блока
        self.FORMAT = pyaudio.paInt16   # Формат данных
        self.CHANNELS = 1               # Количество каналов
        self.RATE = 44100               # Частота дискретизации
        self.streamed = False           # Проверка запуска потока
        self.thread = None              # Поток со звуком
        self.callback = None            # Функция обратного вызова
    
    def set_callback(self, callback):
        """Устанавливаем функцию обратного вызова
        """
        self.callback = callback

    def start_stream(self):
        """Запускаем поток для входа/выхода аудио
        """
        self.p = pyaudio.PyAudio()
        self.streamed = True
        self.stream = self.p.open(
            format = self.FORMAT,
            channels = self.CHANNELS,
            rate = self.RATE,
            input = True,
            output = True,
            input_device_index=1,
            output_device_index=2,
            frames_per_buffer = self.CHUNK,
        )

        self.thread = threading.Thread(target=self._start_audio)
        self.thread.daemon = True
        self.thread.start()
    
    def _start_audio(self):
        while self.streamed:
            data = self.stream.read(self.CHUNK)
            if self.callback:
                self.callback(data)
            self.stream.write(data)

    def stop_stream(self):
        """Останавливаем поток
        """
        self.streamed = False
        if hasattr(self, "stream"):
            self.stream.stop_stream()
            self.stream.close()
        if hasattr(self, "p"):
            self.p.terminate()

    
if __name__ == '__main__':
    # Проверка работы ввода и вывода аудио
    audio_stream = AudioStream()
    audio_stream.start_stream()
    time.sleep(5)
    audio_stream.stop_stream()

