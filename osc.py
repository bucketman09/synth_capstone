import numpy as np

class Osc:

    def __init__(self):
        self
        
    def generate_wf(self, wave_type, amp, freq, t_values):
        if wave_type == 0:
            wave = amp * np.sin(2 * np.pi * freq * t_values)
        elif wave_type == 1:
            wave = amp * (np.abs(np.sin(2 * np.pi * freq * t_values))/(np.sin(2 * np.pi * freq * t_values)))
            
        return wave
    
