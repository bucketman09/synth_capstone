from GUI import GUI
from gpiozero import RotaryEncoder, Button
#from synth import Synth

class InputController:
    def __init__(self, gui, not_selected):
        self.rotor = RotaryEncoder(10,9,wrap=True)
        self.rotor_btn = Button(11)
        self.not_selected = not_selected
        #self.synth.s_index = 0
        #self.s_max_index = 5
        
        self.gui = gui
        #self.synth = synth
        
        self.rotor.when_rotated_clockwise = self.right
        self.rotor.when_rotated_counter_clockwise = self.left
        self.rotor_btn.when_pressed = self.pressed

    def left(self):
        #print("left")
        if self.gui.menu_index <= 1:
            self.rotate_selection(True)
        
    def right(self):
        #print("right")
        if self.gui.menu_index <= 1:
            self.rotate_selection(False)
                    
    def rotate_selection(self,is_left):
        print(len(self.gui.options))
        if is_left:
            self.gui.s_index = self.gui.s_index - 1
            if self.gui.s_index < 0:
                self.gui.s_index = 0
        else:
            self.gui.s_index = self.gui.s_index + 1
            if self.gui.s_index > len(self.gui.options):
                self.gui.s_index = len(self.gui.options)
                
        self.gui.settings_menu()
            

    def pressed(self):
        self.not_selected()
        self.gui.menu_index = self.gui.menu_index + 1
        
                
                
        
