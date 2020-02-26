from sine_generator import SineGenerator
from tc_generator import TCGenerator
from IOstream import IOStream
import wave as wv
import numpy as np
import matplotlib.pyplot as plt
from bitarray import bitarray
import sys

##### Sine Generator Test
generator = SineGenerator(freq=30)
wave = generator.audioData(duration=1000*66)

waveFile = wv.open('test.wav', 'wb')
waveFile.setnchannels(1)
waveFile.setsampwidth(2)
waveFile.setframerate(44100)
waveFile.writeframes(wave)
waveFile.close()

##### TC Generator Test
generatorTC = TCGenerator()

wave = generatorTC.audioData(duration=5000)

waveFile = wv.open('testTC.wav', 'wb')
waveFile.setnchannels(1)
waveFile.setsampwidth(2)
waveFile.setframerate(44100)
waveFile.writeframes(np.array(wave).tobytes())
waveFile.close()

##### TC Read
waveFile = wv.open('ltc.wav', 'rb')
data = waveFile.readframes(waveFile.getnframes())
# print(waveFile.getparams())
# print(data)
# print(testData)
# print((int.from_bytes(data[0], byteorder='big')))
# print(list(data))
waveFile = wv.open('testLTC.wav', 'wb')
waveFile.setnchannels(1)
waveFile.setsampwidth(2)
waveFile.setframerate(44100)
waveFile.writeframes(data[4000:])
waveFile.close()


##### IOStream
stream = IOStream()

stream.stamp_wav(inputFile='test.wav')