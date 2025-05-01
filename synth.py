import rtmidi
#import pyaudio
import sounddevice as sd
import numpy as np

#from machine import I2C, Pin
#from gpiozero import RotaryEncoder, Button
from note import Note
from adsr_envelope import Env
from osc import Osc
from GUI import GUI
from input_controller import InputController

class Synth:
    def __init__(self, RATE, CHUNK):
        self.RATE = RATE
        self.CHUNK = CHUNK
        
        """
        self.menu_index = 0 # 0 - settings, 1 - draw_wave, 2 - select_menu, 3 - adsr_menu, 4 - osc_menu
        self.s_index = 0
        self.max_index = 0
        """
        
        self.midi_in = rtmidi.MidiIn()
        self.gui = GUI(RATE, CHUNK)
        self.input_cont = InputController(self.gui,self.not_selected)
        self.adsr = Env(.2,.5,.5,1)
        self.midi_in = rtmidi.MidiIn()
        self.oscillators = [Osc(0,1), Osc(1,.5)]
        
        self.selected = False
        self.setup(True)
        
        self.stream.start()
        
        self.synth_loop()
        
    def not_selected(self):
        print("not_selected")
        self.selected = not self.selected
        
    def setup(self,manual):
        if manual:
            #load audio device options into gui array
            self.gui.options = sd.query_devices()
            print(sd.query_devices())
            #draw initial menu
            self.gui.settings_menu()
            #hold program untill button press
            while self.selected == False:
                pass
            
            #assign default sound device to current selection index 
            sd.default.device = self.gui.s_index
            self.stream = sd.OutputStream(samplerate = self.RATE, blocksize = self.CHUNK, channels = 1, dtype = 'int16')
            
            #reset bool
            self.selected == False
            #load midi ports into options array
            self.gui.options = self.midi_in.get_ports()
            print(self.midi_in.get_ports())
            #draw initial menu
            self.gui.settings_menu()
            #hold
            print(self.selected)
            while self.selected == False:
                pass
            
            #set midi device to s_index
            midi_device_index = self.gui.s_index
            self.midi_in.open_port(midi_device_index)
            self.selected = True
        
    def synth_loop(self):
        if self.midi_in.is_port_open():
            print("port open")
            note_value = 0
            note_velocity = 0
            
            t = 0
            amp = 0
            notes = []
            wave = np.zeros(self.CHUNK)
            
            while True:
                #get latest midi
                msg_and_t = self.midi_in.get_message()
                
                #if there is a message get the values
                if msg_and_t:
                    (msg, dt) = msg_and_t
                    channel = hex(msg[0])
                    #print(channel)
                    note_value = msg[1]
                    note_velocity = msg[2]
                    if note_velocity == 0:
                        for note in notes:
                            if note.value == note_value:
                                note.pressed = False
                                note.time_set = t/self.RATE     
                    else:
                        note = Note(note_value, note_velocity,t/self.RATE,channel,True,0)
                        notes.append(note)
                
                t_values = (np.arange(self.CHUNK) + t) / self.RATE
                
                #iterate through current notes apply filters and oscs and add the wave forms together
                wave = np.zeros(self.CHUNK)
                for note in notes:
                    #if note.channel == 0x9 or 0x8:
                    gain = self.adsr.apply(note,t/self.RATE)
                    if gain < 0:
                        note.velocity = -1
                        #notes.remove(note)
                    else:
                        freq = 440 * 2 ** ((note.value - 69)/12)
                        amp = int(32767 * (note.velocity / 127.0)) * gain
                        
                    for osc in self.oscillators:
                        wave += osc.generate_wf(amp, freq, t_values)
                        
                #if draw_wave_bool: 
                    #gui.draw_wave(wave)
                
                #normalize amp
                if len(notes) != 0: 
                    wave = wave / (len(notes) * len(self.oscillators))
                    
                wave = wave.astype(np.int16)
                
                self.stream.write(wave)
                
                #prevent excesive t size
                #if np.all(wave == 0):
                #    t = 0
                    
                t += self.CHUNK
                
                for note in notes[:]:
                    if note.velocity == -1:
                        notes.remove(note)
                        
synth = Synth(44100,256)
synth.synth_loop()
        
                
        
    