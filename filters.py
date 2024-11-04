from scipy import signal
import numpy as np

class SignalFilter:
    def __init__(self, sample_rate=44100):
        self.fs = sample_rate
        self.nyquist = self.fs / 2

    def create_lowpass(self, cutoff_freq):
        return signal.butter(4, cutoff_freq/self.nyquist, btype="lowpass")
    
    def create_highpass(self, cutoff_freq):
        return signal.butter(4, cutoff_freq/self.nyquist, btype="highpass")

    def create_bandpass(self, lowcut, highcut):
        return signal.butter(4, [lowcut/self.nyquist, highcut/self.nyquist], btype="bandpass")
    
    def create_bandstop(self, lowcut, highcut):
        return signal.butter(4, [lowcut/self.nyquist, highcut/self.nyquist], btype="bandstop")
    
    def apply_filter(self, data, filter_type, low_freq=None, high_freq=None):
        if filter_type is None:
            return data

        match filter_type:
            case "lowpass":
                b, a = self.create_lowpass(low_freq)
            case "highpass":
                b, a = self.create_highpass(high_freq)
            case "bandpass":
                b, a = self.create_bandpass(low_freq, high_freq)
            case "bandstop":
                b, a = self.create_bandstop(low_freq, high_freq)
        
        return signal.filtfilt(b, a, data)

