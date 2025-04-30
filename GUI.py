from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306#, ssd1325, ssd1331, sh1106
#import numpy as np

class GUI:
    def __init__ (self, CHUNK, AMP):
        self.chunk = CHUNK
        self.s_w = 128
        self.s_h = 64
        self.x_r = (CHUNK/self.s_w)
        self.y_r = ((self.s_h/2) / AMP)
        
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial, rotate=0)
        
    #allow user to scroll through options - adsr, osc
    def select_menu():
        with canvas(self.device) as draw:
            draw.text("select menu")
        
    #allow user to select osc and change wave_form and level
    def osc_menu():
        with canvas(self.device) as draw:
            draw.text("osc menu ")
            
    #allow user to select adsr levels    
    def adsr_menu():
        with canvas(self.device) as draw:
            draw.text("adsr menu")
        
    def draw_wave(self, wave):
        graph = []
        
        if wave != Empty:
            for i in range(int(self.s_w - self.x_r)):
                #new_y = (wave[i] + wave[int(i + self.x_r)])/2
                #graph.append(i, (new_y * (screen[i] * self.y_r) + 32))
                
                new_y = (wave[i] + wave[int(i + self.x_r)])/2
                graph.append((i, int(((new_y * self.y_r) + 32))))
                
            #print(graph)
               
            with canvas(self.device) as draw:
                    draw.point(graph, fill="white")
            
        
      

        
        
        

