from input_controller import InputController
from GUI import GUI
from synth import Synth
import rtmidi
import sounddevice

gui = GUI()
input_controller = input_controller(gui)

synth = Synth(44100, 256)

gui.options = sd.query_devices()
gui.settings_menu(0)





