from gpiozero import Button, RotaryEncoder
from signal import pause

rotor = RotaryEncoder(10,9,wrap=True)
rotor_btn = Button(11)

def pressed():
    print("pressed")
    
def left():
    print("left/down")
    
def right():
    print("right/up")
    
rotor.when_rotated_clockwise = right
rotor.when_rotated_counter_clockwise = left
rotor_btn.when_pressed = pressed

pause()
    