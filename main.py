import rtmidi
#import pyaudio
import sounddevice as sd
import numpy as np

#from machine import I2C, Pin
from gpiozero import RotaryEncoder, Button
from note import Note
from adsr_envelope import Env
from osc import Osc
#from GUI import GUI

adsr = Env(.2,.5,.5,1)
midi_in = rtmidi.MidiIn()

RATE = 44100
CHUNK = 256
amp = 32767
freq = 440

#screen_bools

select_menu_bool = False
osc_menu_bool = False
adsr_menu_bool = False
draw_wave_bool = True

#gui = GUI(CHUNK,amp)

oscillators = [Osc(0,1), Osc(1,.5)]

print(sd.query_devices())
device_index = int(input("select audio device (starting at index 0)"))
sd.default.device = device_index

stream = sd.OutputStream(samplerate = RATE, blocksize = CHUNK, channels = 1, dtype = 'int16')
stream.start()

#p = pyaudio.PyAudio()

#for i in range(p.get_device_count()):
    #info = p.get_device_info_by_index(i)
    #print(f"{i}: {info['name']} - Output Channels: {info['maxOutputChannels']}")
#print(p.get_device_info_by_index(3))
#device_index = int(input("select audio device (starting at index 0)"))

#stream = p.open(format=pyaudio.paInt16, channels=2, rate = RATE, input=False,
#                output=True, frames_per_buffer=CHUNK, output_device_index = device_index)

print(midi_in.get_ports())
midi_device = int(input("Select midi device (Starting index 0)"))
#num_aud_osc = int(input("Num of osc (starting at amt 1)"))

try:
    midi_in.open_port(midi_device)
except Exception as e:
    print("no midi instruments detected")


if midi_in.is_port_open():
    print("port open")
    
    #pressed = False
    note_value = 0
    note_velocity = 0
    
    t = 0
    
    amp = 0
    
    notes = []
    
    while True:
        """
        if select_menu_bool:
            print("select menu")
        elif osc_menu_bool:
            print("osc menu")
        elif adsr_menu_bool:
            print("adsr menu")
            """
        
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
        
        #iterate through current notes apply filters and oscs and add the wave forms together
        wave = np.zeros(CHUNK)
        for note in notes:
            #if note.channel == 0x9 or 0x8:
            gain = adsr.apply(note,t/RATE)
            if gain < 0:
                note.velocity = -1
                #notes.remove(note)
            else:
                freq = 440 * 2 ** ((note.value - 69)/12)
                amp = int(32767 * (note.velocity / 127.0)) * gain
                
            for osc in oscillators:
                wave += osc.generate_wf(amp, freq, t_values)
                
        #if draw_wave_bool: 
            #gui.draw_wave(wave)
        
        #normalize amp
        if len(notes) != 0: 
            wave = wave / (len(notes) * len(oscillators))
            
        wave = wave.astype(np.int16)
        
        stream.write(wave)
        
        #prevent excesive t size
        #if np.all(wave == 0):
        #    t = 0
            
        t += CHUNK
        
        for note in notes:
            if note.velocity == -1:
                notes.remove(note)
                
#stream.stop_stream()
stream.stop()
stream.close()
#p.terminate()