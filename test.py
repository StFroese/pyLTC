from sine_generator import SineGenerator
import wave as wv
import numpy as np

#96kHz/24Bit testen

generator = SineGenerator(freq=100)

wave = generator.wave(duration=5000)
wave = (wave * (2**16 - 1)).astype(np.uint16)
print(wave.dtype)
print(len(wave))
wave = wave.tobytes()
print(len(wave))


waveFile = wv.open('test.wav', 'wb')
waveFile.setnchannels(1)
waveFile.setsampwidth(2)
waveFile.setframerate(44100)
# waveFile.setnframes(44100*5)
waveFile.writeframes(wave)
waveFile.close()



