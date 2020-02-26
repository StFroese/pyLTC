import math
import itertools
import numpy as np

class SineGenerator:

    def __init__(self, sampleRate=44100, bitDepth=16, freq=100):
        self.sampleRate = sampleRate
        self.bitDepth = bitDepth
        self.freq = freq

    def generate(self):
        sample = 0
        while True:
            yield math.sin(2 * math.pi * self.freq / self.sampleRate * sample)
            sample += 1

    def wave(self):
        wave = []
        for val in itertools.islice(self.generate(), int(self.sampleRate*self.duration/1000)):
            wave.append(val)
        return np.array(wave)  

    def audioData(self, duration=1000):  #duration in ms
        self.duration = duration
        wave = self.wave()
        wave = (wave * ((2**16)/2 - 1)).astype(np.int16)
        return wave.tobytes()      


        



