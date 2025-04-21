from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import numpy as np

class GUI:
    def __init__ (self, CHUNK, AMP):
        self.chunk = CHUNK
        self.s_w = 128
        self.s_h = 64
        self.x_r = (CHUNK/s_w)
        self.y_r = ((s_h/2) / AMP)
        
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial, rotate=0)
        
    def draw_wave(self, wave):
        #x_r = 256/128
        #y_r = 32/amp
        screen = np.zeros(chunk)
        
        for i in range(len(screen)):
            screen[i] = (wave[i] + wave[int(i + self.x_r)])/2
            screen[i] = (screen[i] * self.y_r) + 32
           
        with canvas(self.device) as draw:
                draw.point(graph, fill="white")
            
        
      

        
        
        

