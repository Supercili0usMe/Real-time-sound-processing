from ui.main_window import Ui_MainWindow
from audio_processor import AudioStream
from visualizer import AudioVisualizer
from filters import SignalFilter
from PyQt6 import QtWidgets, QtCore
import pyaudio
import numpy as np
import pyqtgraph as pg

class AudioProcessor(QtWidgets.QMainWindow, Ui_MainWindow):
    update_signal = QtCore.pyqtSignal(bytes)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_components()
        self.setup_plots()
        self.connect_signals()
        self.setup_frequency_controls()

    def init_components(self):
        """Initialize main components"""
        self.audio_stream = AudioStream()
        self.signal_filter = SignalFilter()
        self.current_filter_type = None

    def setup_plots(self):
        """Configure plot widgets and their settings"""
        # Create new plot widgets
        self.plot_waveform = pg.PlotWidget()
        self.plot_spectrum = pg.PlotWidget()
        
        # Replace old widgets with new plots
        self.graphicsView.deleteLater()
        self.graphicsView_2.deleteLater()
        self.gridLayout_2.addWidget(self.plot_waveform)
        self.gridLayout_2.addWidget(self.plot_spectrum)

        # Configure axes
        self._setup_waveform_axes()
        self._setup_spectrum_axes()
        
        # Initialize visualizer
        self.visualizer = AudioVisualizer(self.plot_waveform, self.plot_spectrum)

    def _setup_waveform_axes(self):
        """Configure waveform plot axes"""
        wf_xlabels = [(0, "0"), (2048, "2048"), (4096, "4096")]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        wf_ylabels = [(0, "0"), (127, "127"), (255, "255")]
        wf_yaxis = pg.AxisItem(orientation='left')
        wf_yaxis.setTicks([wf_ylabels])

        self.plot_waveform.setAxisItems({'bottom': wf_xaxis, 'left': wf_yaxis})

    def _setup_spectrum_axes(self):
        """Configure spectrum plot axes"""
        sp_xlabels = [(np.log10(10), "10"), (np.log10(100), "100"),
                      (np.log10(1000), "1000"), (np.log10(22050), "22050")]
        sp_xaxis = pg.AxisItem(orientation='bottom')
        sp_xaxis.setTicks([sp_xlabels])
        self.plot_spectrum.setAxisItems({'bottom': sp_xaxis})

    def setup_frequency_controls(self):
        """Set up frequency range controls"""
        self.spin_freq_low.setRange(20, 20000)
        self.spin_freq_high.setRange(20, 20000)

    def connect_signals(self):
        """Connect all UI signals to their handlers"""
        self.btn_start.clicked.connect(self.start_audio)
        self.btn_stop.clicked.connect(self.stop_audio)
        self.update_signal.connect(self.update_visualizer)
        
        # Connect filter buttons
        self.btn_low_pass.toggled.connect(self.update_filter)
        self.btn_high_pass.toggled.connect(self.update_filter)
        self.btn_band_pass.toggled.connect(self.update_filter)
        self.btn_band_stop.toggled.connect(self.update_filter)
        self.btn_no_filt.toggled.connect(self.update_filter)

    def start_audio(self):
        """Start audio processing"""
        def audio_callback(in_data, frame_count, time_info, status):
            data = np.frombuffer(in_data, dtype=np.int16)
            
            if self.current_filter_type:
                filtered_data = self.signal_filter.apply_filter(
                    data, 
                    self.current_filter_type,
                    self.spin_freq_low.value(),
                    self.spin_freq_high.value()
                )
                out_data = filtered_data.astype(np.int16).tobytes()
            else:
                out_data = in_data
                
            self.update_signal.emit(out_data)
            return (out_data, pyaudio.paContinue)
        
        self.audio_stream.start_stream(audio_callback)
        print("Поток запущен")

    def stop_audio(self):
        """Stop audio processing"""
        if hasattr(self, 'audio_stream'):
            print("Поток остановлен")
            self.audio_stream.stop_stream()
            self.audio_stream = AudioStream()

    @QtCore.pyqtSlot(bytes)
    def update_visualizer(self, data):
        """Update visualization with new audio data"""
        self.visualizer.update_plots(data)

    def update_filter(self):
        """Update current filter based on selected radio button"""
        if self.btn_no_filt.isChecked():
            self.current_filter_type = None
        elif self.btn_low_pass.isChecked():
            self.current_filter_type = "lowpass"
        elif self.btn_high_pass.isChecked():
            self.current_filter_type = "highpass"
        elif self.btn_band_pass.isChecked():
            self.current_filter_type = "bandpass"
        elif self.btn_band_stop.isChecked():
            self.current_filter_type = "bandstop"

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = AudioProcessor()
    window.show()
    sys.exit(app.exec())
