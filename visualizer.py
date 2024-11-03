from audio_processor import AudioStream
import time
from PyQt6 import QtWidgets
import pyqtgraph as pg
import numpy as np

class AudioVisualizer:
    def __init__(self, graphics_view1, graphics_view2):
        # Настраиваем первый график (временная область)
        self.time_plot = pg.PlotWidget()
        scene1 = QtWidgets.QGraphicsScene()
        scene1.addWidget(self.time_plot)
        graphics_view1.setScene(scene1)

        # Настраиваем второй график (частотная область)
        self.freq_plot = pg.PlotWidget()
        scene2 = QtWidgets.QGraphicsScene()
        scene2.addWidget(self.freq_plot)
        graphics_view2.setScene(scene2)

        # Настройка графиков
        self.time_curve = self.time_plot.plot(pen="g")
        self.freq_curve = self.freq_plot.plot(pen="r")

        # Настройка осей и заголовков
        self.time_plot.setTitle("Временная область")
        self.freq_plot.setTitle("Частотная область")
    
    def update_plots(self, audio_data):
        """Обновляем данные на графиках
        """
        # Обновление временной области
        waveform = np.frombuffer(audio_data, dtype=np.int16)
        self.time_curve.setData(waveform)

        # Обновление частотной области
        spectrum = np.abs(np.fft.fft(waveform))
        self.freq_curve.setData(spectrum[:len(spectrum)//2])
