import time
import rtmidi
import pyaudio
import numpy as np

from pyblaster_adsr_envelope import Env
from osc import Osc

adsr = Env(.5,.5,.2,1.5)
midi_in = rtmidi.MidiIn()

print(midi_in.get_ports())

RATE = 44100
CHUNK = 256
amp = 32767
freq = 440

osc = Osc(0)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate = RATE, input=True, output=True, frames_per_buffer=CHUNK)

pressed = False

try:
    midi_in.open_port(0)
except Exception as e:
    print("no midi instruments detected")

if midi_in.is_port_open():
    print("port open")
        
    note_value = 0
    note_velocity = 0
    
    t = 0
    
    amp = 0
    
    notes = []
    
    while True:
        #get latest midi
        msg_and_t = midi_in.get_message()
        
        #if there is a message get the values
        if msg_and_t:
            (msg, dt) = msg_and_t
            #print(dt)
            #channel = hex(msg[0])
            note_value = msg[1]
            note_velocity = msg[2]
            if note_velocity == 0:
                for note in notes[:]:
                    if note[0] == note_value:
                        notes.remove(note)
            else:
                
                notes.append((note_value,note_velocity))
                #print(len(notes))
        
        t_values = (np.arange(CHUNK) + t) / RATE
        
        #iterate through current notes and add the wave forms together
        wave = np.zeros(CHUNK)
        for note in notes:
            freq = 440 * 2 ** ((note[0] - 69)/12)
            amp = int(32767 * (note[1] / 127.0))
            #adsr.apply(True)
            
            wave += osc.generate_wf(amp, freq, t_values)
            
        wave -= np.mean(wave)
        
        #normalize
        if np.max(np.abs(wave)) > 32767:
            wave = (wave / np.max(np.abs(wave))) * 32767
            
        wave = wave.astype(np.int16)
        
        
        stream.write(wave.tobytes())

        t += CHUNK
        
            
        """
        #determine freq from note_value
        if note_velocity > 0: 
            pressed = True
        else:
            pressed = False
            
        #if len(notes) > 0:
            #print(len(notes))
          
            
        freq = 440 * 2 ** ((note_value - 69)/12)
        amp = int(32767 * (note_velocity / 127.0))
            
        gain = adsr.apply(pressed)
        
        amp = gain * amp
        
        t_values = (np.arange(CHUNK) + t) / RATE
        
        sine_wave = (amp * np.sin(2 * np.pi * freq * t_values)).astype(np.int16)

        #stream.write(sine_wave.tobytes())

        t += CHUNK
        """
                   
stream.stop_stream()
stream.close()
p.terminate()
        