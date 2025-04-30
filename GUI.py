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
        
        self.menu_index = 0 # 0 - audio settings_menu,1 - midi settings_menu midi, 2 - draw_wave, 3 - select_menu, 4 - adsr_menu, 5 - osc_menu
        self.s_index = 0
        self.options = []
    
    #select audio and midi device - runs on start
    def settings_menu(self):
        print(self.s_index)
        with canvas(self.device) as draw:
            if self.menu_index == 0:
                option = str(self.options[self.s_index]['name'])
            elif self.menu_index == 1
                option = str(self.options[self.s_index])
            draw.text((0,32), option, fill=255)
            
    #allow user to scroll through options - adsr, osc
    def select_menu(self):
        with canvas(self.device) as draw:
            draw.text("select menu")
        
    #allow user to select osc and change wave_form and level
    def osc_menu(self):
        with canvas(self.device) as draw:
            draw.text("osc menu ")
            
    #allow user to select adsr levels    
    def adsr_menu(self):
        with canvas(self.device) as draw:
            draw.text("adsr menu")
        
    def draw_wave(self, wave):
        graph = []
        
        for i in range(int(self.s_w - self.x_r)):
            #new_y = (wave[i] + wave[int(i + self.x_r)])/2
            #graph.append(i, (new_y * (screen[i] * self.y_r) + 32))
            
            new_y = (wave[i] + wave[int(i + self.x_r)])/2
            graph.append((i, int(((new_y * self.y_r) + 32))))
            
        #print(graph)
           
        with canvas(self.device) as draw:
            draw.point(graph, fill="white")
            
        
      

        
        
        

