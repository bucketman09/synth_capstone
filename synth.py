import pyaudio

class Synth:
    
    def __init__(self, RATE, CHUNK):
        self.RATE = RATE
        self.CHUNK = CHUNK
        
        self.p = pyaudio.PyAudio()
        self.stream = (format=pyaudio.paInt16, channels=1, rate = RATE, input=False, output=True, frames_per_buffer=CHUNK)
    
    def synth_start(self):
        
        
    