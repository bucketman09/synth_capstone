import time

class Env:
    
    def __init__(self, a = 0, d = 0, s = 0, r = 0, g = .5):
        self.a_phase = a
        self.d_phase = d
        self.s_level = s
        self.r_phase = r
        self.gain = g
        
        self.level = 0
        self.p_start_time = 0.0
        self.r_start_time = 0.0
        self.pressed_time = 0.0
        self.released_time = 0.0
        
    def apply(self, pressed):

        if pressed:
            self.pressed_time = time.time() - self.p_start_time
            self.r_start_time = time.time()
            self.released_time = 0
            
            #attack
            if self.pressed_time <= self.a_phase:
                self.level = (self.pressed_time / self.a_phase) * self.gain
            
            #decay
            elif self.pressed_time <= self.a_phase + self.d_phase:
                self.level = self.gain - (self.pressed_time - self.a_phase) / self.d_phase * (self.gain - (self.gain * self.s_level))
            
            #sustain
            elif self.pressed_time > self.a_phase + self.d_phase:
                self.level = self.s_level * self.gain
                
                

        else:
            self.released_time = time.time() - self.r_start_time
            self.p_start_time = time.time()
            self.pressed_time = 0
            
            fraction = self.level * self.gain
            
            if self.level > 0.001 and self.r_phase > 0:
                self.level = (self.r_phase * fraction - self.released_time) / (
                            self.r_phase * fraction) * self.level
            else:
                self.level
    
            
        
        
        return self.level
        
