import gpiozero

class InputController

    def __init__(self):
        self.rotor = RotaryEncoder(10,9,wrap=True)
        self.rotor_btn = Button(11)
        self.menu_index = 0 #00 - settings_menu, 1 - draw_wave, 2 - select_menu, 3 - adsr_menu, 4 - osc_menu
        self.s_index = 0
        self.s_max_index = 5
        
        self.rotor.when_rotated_clockwise = self.right
        self.rotor.when_rotated_counter_clockwise = self.left
        self.rotor_btn.when_pressed = self.pressed

    def left(self):
        self.menu_index
        match self.menu_index:
            case 0:
                self.s_index -=
                if self.s_index < 0:
                    self.s_index = 0
                
            
        
    def right(self):
        self.menu_index
        match self.menu_index:
            case 0:
                self.s_index +=
                if self.s_max_index > 0:
                    self.s_index = self.s_max_index

    def pressed(self):
        self.menu_index
        match self.menu_index:
            case 0:
                self.menu_index = 1
        print("pressed")
        
