import sys
import time
import pyaudio
import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt
from pyqtgraph.Qt import QtGui, QtCore

class AudioStream(object):
    def __init__(self):
        # Используемые константы
        self.CHUNK = 1024 * 2
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.pause = False

        # Объект потока
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.FORMAT,
            channels = self.CHANNELS,
            rate = self.RATE,
            input = True,
            output = True,
            frames_per_buffer = self.CHUNK
        )

        # Переменные для графиков
        self.x = np.arange(0, 2 * self.CHUNK, 2)
        self.x_fft = np.linspace(0, self.RATE, self.CHUNK)


        # Параметры для создания графиков
        self.traces = dict()
        self.app = QtGui.QGuiApplication(sys.argv)
        self.win = pg.GraphicsLayout()
        self.win.setWindowTitle('Анализатор спектра')
        self.win.setGeometry(5, 115, 1910, 1070)

        wf_xlabels = [(0, '0'), (2048, "2048"), (4096, "4096")]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        wf_ylabels = [(0, '0'), (127, "127"), (255, "255")]
        wf_yaxis = pg.AxisItem(orientation='left')
        wf_yaxis.setTicks([wf_ylabels])

        sp_xlabels = [(np.log10(10), "10"), (np.log10(100), "100"),
                      (np.log10(1000), "1000"), (np.log10(22050), "22050")]
        sp_xaxis = pg.AxisItem(orientation='bottom')
        sp_xaxis.setTicks([sp_xlabels])

        self.waveform = self.win.addPlot(
            title='waveform', row=1, col=1, axisItems={'bottom': wf_xaxis, 'left': wf_yaxis}
        )
        self.spectrum = self.win.addPlot(
            title="spectrum", row=2, col=1, axisItems={'bottom': sp_xaxis}
        )

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, "PYQT_VERSION"):
            QtGui.QGuiApplication.instance().exec_()

    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setY(0, 255, padding = 0)
                self.waveform.setX(0, 2 * self.CHUNK, padding=.005)
            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen="m", width=3)
                self.spectrum.setLogMode(x=True, y=True)
                self.spectrum.setX(-4, 0, padding=0)
                self.spectrum.setY(np.log10(20), np.log10(self.RATE / 2), padding=.005)
    
    def update(self):
        wf_data = self.stream.read(self.CHUNK)
        wf_data = np.frombuffer(wf_data, dtype=np.int16) + 128
        self.set_plotdata(name="waveform", data_x=self.x, data_y=wf_data)

        sp_data = np.ffr.fft(wf_data - 128)
        sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]) * 2 /(128 * self.CHUNK)
        self.set_plotdata(name='spectrum', data_x=self.x_fft, data_y=sp_data)

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()

if __name__ == '__main__':
    audio_app = AudioStream()
    audio_app.animation()