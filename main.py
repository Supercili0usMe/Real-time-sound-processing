from ui.main_window import Ui_MainWindow
from audio_processor import AudioStream
from visualizer import AudioVisualizer
from PyQt6 import QtWidgets, QtCore
import numpy as np

class AudioProcessor(QtWidgets.QMainWindow, Ui_MainWindow):
    update_signal = QtCore.pyqtSignal(bytes)    # Сигнал для обновления графиков

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Создаем экземпляры классов
        self.audio_stream = AudioStream()
        self.visualizer = AudioVisualizer(self.graphicsView, self.graphicsView_2)

        # Настройка начальных значений спинбоксов
        self.spin_freq_low.setRange(20, 20000)
        self.spin_freq_high.setRange(20, 20000)

        # Подключение сигналов к обработчикам
        self.btn_start.clicked.connect(self.start_audio)
        self.btn_stop.clicked.connect(self.stop_audio)
        self.btn_low_pass.toggled.connect(self.update_filter)
        self.btn_high_pass.toggled.connect(self.update_filter)
        self.btn_band_pass.toggled.connect(self.update_filter)
        self.btn_band_stop.toggled.connect(self.update_filter)
        self.btn_no_filt.toggled.connect(self.update_filter)

        self.update_signal.connect(self.update_visualizer)
    
    def start_audio(self):
        def audio_callback(data):
            self.update_signal.emit(data)
        
        self.audio_stream.set_callback(audio_callback)
        self.audio_stream.start_stream()
        print("Запуск потока звука")

    def stop_audio(self):
        self.audio_stream.stop_stream()
        print("Остановка потока звука")

    @QtCore.pyqtSlot(bytes)
    def update_visualizer(self, data):
        self.visualizer.update_plots(data)
    
    def update_filter(self):
        if self.btn_no_filt.isChecked():
            print("Режим без фильтра")
        elif self.btn_low_pass.isChecked():
            print("Режим ФНЧ")
        elif self.btn_high_pass.isChecked():
            print("Режим ФВЧ")
        elif self.btn_band_pass.isChecked():
            print("Режим полосового фильтра")
        elif self.btn_band_stop.isChecked():
            print("Режим режекторного фильтра")



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = AudioProcessor()
    window.show()
    sys.exit(app.exec())