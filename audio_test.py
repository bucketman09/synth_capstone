"""
import pyaudio

try:
    p = pyaudio.PyAudio()
except:
    print("error")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"{i}: {info['name']} - Output Channels: {info['maxOutputChannels']}")



stream = p.open(format=pyaudio.paInt32, channels=2, rate = RATE, output=True, output_device_index = 0, frames_per_buffer=CHUNK)

print("succes?")
"""
import pyaudio
import sounddevice as sd
import numpy as np

RATE = 44100
CHUNK = 256
t=0

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"{i}: {info['name']} - Output Channels: {info['maxOutputChannels']}")
device_index = int(input("select devices (starting at index 0)"))
stream = p.open(format=pyaudio.paInt16, channels=1, rate = RATE, input=False, output=True, frames_per_buffer=CHUNK, output_device_index = device_index)

#print(sd.query_devices())
#device_index = int(input("select devices (starting at index 0)"))
#sd.default.device = device_index
#stream = sd.OutputStream(samplerate = RATE, blocksize = CHUNK, channels = 1, dtype = 'int16')
#stream.start()

while True:
    t_values = (np.arange(CHUNK) + t) / RATE
    wave = 32767 * np.sin(2 * np.pi * 440 * t_values)
    wave = wave.astype(np.int16)
    

    stream.write(wave)
    t += CHUNK