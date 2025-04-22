import pyaudio

try:
    p = pyaudio.PyAudio()
except:
    print("error")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"{i}: {info['name']} - Output Channels: {info['maxOutputChannels']}")

RATE = 44100
CHUNK = 256

#stream = p.open(format=pyaudio.paInt16, channels=1, rate = RATE, input=False, output=True, frames_per_buffer=CHUNK)

print("succes?")