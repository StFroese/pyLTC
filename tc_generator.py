from bitarray import bitarray
import itertools
import numpy as np

class TCGenerator:
    
    def __init__(self, sampleRate=44100, bitDepth=16, frameRate=30):
        self.sampleRate = sampleRate
        self.bitDepth = bitDepth
        self.frameRate = frameRate

    def generate(self):
        sample = 0
        sf_ratio = self.sampleRate/self.frameRate #1470
        while True:
            yield int(sample/sf_ratio)
            sample += 1
            sample = sample % self.sampleRate

    def generateFPS(self):
        frame = 0
        while True:
            yield frame
            frame += 1
            frame = frame % self.frameRate


    def tcRaw(self, frame, second, minute, hour):
        self.frame = frame
        self.second = second
        self.minute = minute
        self.hour = hour

        #split digits in units and tens
        f_units = frame % 10
        f_tens = int((frame/10) % 10)
        s_units = second % 10
        s_tens = int((second/10) % 10)
        m_units = minute % 10
        m_tens = int((minute/10) % 10)
        h_units = hour % 10
        h_tens = int((hour/10) % 10)

        #convert digits to binary
        f_units = format(f_units, '04b')[::-1] #change bit order to 0-1-2-4
        f_tens = format(f_tens, '02b')[::-1]
        s_units = format(s_units, '04b')[::-1]
        s_tens = format(s_tens, '03b')[::-1]
        m_units = format(m_units, '04b')[::-1]
        m_tens = format(m_tens, '03b')[::-1]
        h_units = format(h_units, '04b')[::-1]
        h_tens = format(h_tens, '02b')[::-1]

        #bitarray tc
        tc = bitarray()
        tc.extend(f_units)  #frame number units
        tc.extend('0000')   #user bit 1
        tc.extend(f_tens)   #frame number tens
        tc.extend('0')      #drop frame
        tc.extend('0')      #color frame
        tc.extend('0000')   #user bit 2
        tc.extend(s_units)  #second number units
        tc.extend('0000')   #user bit 3
        tc.extend(s_tens)   #second number tens
        tc.extend('0')      #polarity correction bit?
        tc.extend('0000')   #user bit 4
        tc.extend(m_units)  #minute number units
        tc.extend('0000')   #user bit 5
        tc.extend(m_tens)   #minute number tens
        tc.extend('0')      #polarity correction bit?
        tc.extend('0000')   #user bit 6
        tc.extend(h_units)  #hour number units
        tc.extend('0000')   #user bit 7
        tc.extend(h_tens)   #hour number tens
        tc.extend('0')      #BGF 1
        tc.extend('0')      #polarity correction bit?
        tc.extend('0000')   #user bit 8
        tc.extend('0011111111111101') #sync word

        return tc
        
    def tcBlock(self):
        block = []
        sec = 0
        minute = 0
        hour = 0
        l_val = 0
        for val in itertools.islice(self.generateFPS(), int(self.frameRate*self.duration/1000)):
            if l_val==29 and val==0:
                sec += 1
                if sec==60:
                    sec = 0
                    minute += 1
                    if minute==60:
                        minute = 0
                        hour += 1
                        if hour==24:
                            hour = 0 
            l_val = val
            block.append(self.tcRaw(val, sec, minute, hour))
        return np.array(block)

    def audioData(self, duration=1000): #18.375 bytes/samples per bit --> 1=18samples, 0=19samples
        self.duration = duration
        audio = self.tcBlock()
        audio = audio.flatten()
        down = True
        tc_audio = []
        non_integer_bit = 0
        for bit in audio:
            if bit==False:
                if down==True:
                    zero_down = [-1] * (18 +  3*int(non_integer_bit/7)) #fix for non integer number of bits
                    tc_audio.append(zero_down)
                    down = False
                else:
                    zero_up = [1] * (18 + 3*int(non_integer_bit/7))
                    tc_audio.append(zero_up)   
                    down = True
            else:
                if down==True:
                    one_down_0 = [-1] * (9 + 3*int(non_integer_bit/7))
                    one_down_1 = [1] * 9
                    tc_audio.append(one_down_0)
                    tc_audio.append(one_down_1)
                else:
                    one_up_1 = [1] * 9
                    one_up_0 = [-1] * (9 + 3*int(non_integer_bit/7))
                    tc_audio.append(one_up_1)
                    tc_audio.append(one_up_0)  
            non_integer_bit += 1
            non_integer_bit = non_integer_bit % 8        
        tc_audio = [val for sublist in tc_audio for val in sublist]
        tc_audio = np.array(tc_audio)
        tc_audio = (tc_audio * ((2**16)/2-1) * 0.7).astype(np.int16)
        # return tc_audio.tobytes()
        return tc_audio.tobytes()


