from gpiozero import Button, RotaryEncoder


rotor = RotaryEncoder(10,9)
rotor_btn = Button(11)

def pressed():
    print("pressed")
    
def rotated():
    print(rotor.values)
    
rotor.when_rotated = rotated
    
rotor_btn.when_pressed = pressed

while True: