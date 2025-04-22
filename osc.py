import numpy as np

class Osc:

    def __init__(self, wave_type, level):
        self.wave_type = wave_type
        self.level = level
        
    def generate_wf(self, amp, freq, t_values):
        if self.wave_type == 0:
            wave = amp * np.sin(2 * np.pi * freq * t_values)
        elif self.wave_type == 1:
            wave = amp * (np.abs(np.sin(2 * np.pi * freq * t_values))/(np.sin(2 * np.pi * freq * t_values))) 
            
        return wave * self.level
    
