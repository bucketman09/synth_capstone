import rtmidi
import pyaudio
import numpy as np

from note import Note
from adsr_envelope import Env
from osc import Osc
from GUI import GUI
from osc import Osc

adsr = Env(.5,.5,.5,1)
midi_in = rtmidi.MidiIn()

print(midi_in.get_ports())

RATE = 44100
CHUNK = 256
amp = 32767
freq = 440

gui = GUI(CHUNK,amp)
osc = Osc()
num_aud_osc = 1

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate = RATE, input=False, output=True, frames_per_buffer=CHUNK)

pressed = False

midi_device = int(input("Select device (Starting index 0)"))

try:
    midi_in.open_port(midi_device)
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
            channel = hex(msg[0])
            #print(channel)
            note_value = msg[1]
            note_velocity = msg[2]
            if note_velocity == 0:
                for note in notes:
                    if note.value == note_value:
                        note.pressed = False
                        note.time_set = t/RATE     
            else:
                note = Note(note_value, note_velocity,t/RATE,channel,True,0)
                notes.append(note)
        
        t_values = (np.arange(CHUNK) + t) / RATE
        #print(len(notes))
        #iterate through current notes apply filters and add the wave forms together
        wave = np.zeros(CHUNK)
        for note in notes:
            gain = adsr.apply(note,t/RATE)
            if gain < 0:
                notes.remove(note)
            else:
                freq = 440 * 2 ** ((note.value - 69)/12)
                amp = int(32767 * (note.velocity / 127.0)) * gain
                
                wave += osc.generate_wf(0, amp, freq, t_values)
                
        gui.draw_wave(wave)
        
        #normalize amp
        if len(notes) != 0: 
            wave = wave / (len(notes) * num_aud_osc)
            
        wave = wave.astype(np.int16)
        
        stream.write(wave.tobytes())
        
        #prevent excesive t size
        #if np.all(wave == 0):
        #    t = 0
            
        t += CHUNK
                   
stream.stop_stream()
stream.close()
p.terminate()
        
