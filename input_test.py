from gpiozero import Button, RotaryEncoder

rotor = RotaryEncoder(10,9)
rotor_btn = Button(11)

def pressed():
    print("pressed")
    
pressed = rotor_btn.when_pressed