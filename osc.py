import numpy as np

class Osc:

    def __init__(self, wave_type):
        self
        
    def generate_wf(self, amp, freq, t_values):
        sine_wave = (amp * np.sin(2 * np.pi * freq * t_values)).astype(np.int16)
        return sine_wave
    
