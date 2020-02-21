import math

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

        



