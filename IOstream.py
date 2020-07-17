from tc_generator import TCGenerator
import wave as wv
import os
import array


class IOStream:

    def __init__(self, folder=''):
        self.folder = folder

    def stamp_wav(self, inputFile=''):
        self.file = inputFile
        waveFile = wv.open(self.file, 'rb')
        waveFrames = waveFile.getnframes()
        waveAudio = waveFile.readframes(waveFrames)
        waveFile.close()

        array_type = {1: 'B', 2: 'h', 4: 'l'}[2]
        left = array.array(array_type, waveAudio)[::1]
        timecodeGenerator = TCGenerator()
        timecode = timecodeGenerator.audioData(
                duration=int(waveFrames/44100)*1000)
        right = array.array(array_type, timecode)[::1]
        stereo = left * 2
        stereo[0::2] = left
        stereo[1::2] = right

        waveOut = wv.open(os.path.splitext(self.file)[0] + '_TC.wav', 'wb')
        waveOut.setnchannels(2)
        waveOut.setsampwidth(2)
        waveOut.setframerate(44100)
        waveOut.writeframes(stereo.tobytes())
        waveOut.close()
