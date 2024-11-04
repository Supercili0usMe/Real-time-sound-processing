from audio_processor import AudioStream
import time
from PyQt6 import QtWidgets
import pyqtgraph as pg
import numpy as np

class AudioVisualizer:
    def __init__(self, waveform_plot, spectrum_plot):
        self.waveform_plot = waveform_plot
        self.spectrum_plot = spectrum_plot
        
        # Инициализируем графики
        self.waveform_curve = self.waveform_plot.plot(pen='c', width=3)
        self.spectrum_curve = self.spectrum_plot.plot(pen='m', width=3)
        
        # Setup spectrum plot modes
        self.spectrum_plot.setLogMode(x=True, y=True)
        
        # Constants for FFT
        self.CHUNK = 1024 * 2
        self.RATE = 44100
        
        # Setup data arrays
        self.x = np.arange(0, 2 * self.CHUNK, 2)
        self.x_fft = np.linspace(0, self.RATE // 2, self.CHUNK // 2)
        
        # Set plot ranges
        self.waveform_plot.setYRange(0, 255)
        self.waveform_plot.setXRange(0, 2 * self.CHUNK)
        self.spectrum_plot.setXRange(np.log10(20), np.log10(self.RATE/2))
        self.spectrum_plot.setYRange(-4, 0)

    def update_plots(self, data):
        wf_data = (np.frombuffer(data, dtype=np.int16) + 128) % 255
        self.waveform_curve.setData(self.x, wf_data)
        
        sp_data = np.fft.fft(wf_data - 128)
        sp_data = np.abs(sp_data[0:int(self.CHUNK/2)]) * 2 / (128 * self.CHUNK)
        self.spectrum_curve.setData(self.x_fft, sp_data)

