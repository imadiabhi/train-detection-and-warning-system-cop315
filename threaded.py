import pyaudio
import wave
import scipy.io.wavfile as wav
import numpy as np
import math
from threading import Thread
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
TRIG1=23
ECHO1=24
TRIG2=8
ECHO2=7
LED=25
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)
flag = False
var = 0

audiotrig = 0
ultratrig = 0

class Recorder(object):
    '''A recorder class for recording audio to a WAV file.
    Records in mono by default.
    '''
    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,self.frames_per_buffer)

class RecordingFile(object):
    def __init__(self, fname, mode, channels, rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        self._stream = self._pa.open(format=pyaudio.paInt16,channels=self.channels,rate=self.rate,input=True,
                                        frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback

    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile

def mean2(x):
    y = np.sum(x) / np.size(x);
    return y

def corr2(a,b):
    a = a - mean2(a)
    b = b - mean2(b)
    r = (a*b).sum() / math.sqrt((a*a).sum() * (b*b).sum());
    return r

def audio_check():
    while(1):
        rec = Recorder(channels=2)
        with rec.open('recorded_sound.wav', 'wb') as recfile:
        	recfile.record(duration=6.1)
        (rate,t19) = wav.read("19.wav")    
        (rate,t37) = wav.read("37.wav")
        (rate,t) = wav.read("recorded_sound.wav")
        t=t[0:264600]
        t19 = t19/32767.0
        t37 = t37/32767.0
        t = t/32767.0
        t19e = abs(np.fft.fft(t19.T))
        t37e = abs(np.fft.fft(t37.T))
        te = abs(np.fft.fft(t.T))
        R1 = corr2(t37e,te)
        R2 = corr2(t19e,te)
        # print(R)
        # if(R>0.65):
        #     print("Train is Here")
        if(R1>0.65 or R2>0.65):
            audiotrig=1
        else:
            audiotrig=0


##################looped_hc04_ordered###############

def ultra_check():
    while(1):
        print("start")
        #GPIO.output(LED,flag)
        GPIO.output(TRIG1,False)
        time.sleep(0.02)
        GPIO.output(TRIG1,True)
        time.sleep(0.001)
        GPIO.output(TRIG1,False)
        while GPIO.input(ECHO1)==0:
            pulse_start1 = time.time()
        while GPIO.input(ECHO1)==1:
            pulse_end1 = time.time()
        pulse_duration1 = pulse_end1 - pulse_start1

        GPIO.output(TRIG2,False)
        time.sleep(0.02)
        GPIO.output(TRIG2,True)
        time.sleep(0.001)
        GPIO.output(TRIG2,False)
        while GPIO.input(ECHO2)==0:
            pulse_start2 = time.time()
        while GPIO.input(ECHO2)==1:
            pulse_end2 = time.time()
        pulse_duration2 = pulse_end2 - pulse_start2

        distance1 = pulse_duration1 * 17150
        distance2 = pulse_duration2 * 17150

        distance1 = round(distance1, 2)
        distance2 = round(distance2, 2)
        print(distance1)
        print(distance2)
        if(distance1<200 and distance2>200):
            flag=False
            var=1
            ultratrig=0
        elif(distance1<200 and distance2<200 and var==1):
            #GPIO.output(LED,True)
            #print("LED ON")
            ultratrig=1
            time.sleep(1)                    #-------------------------------------------check
            flag = True
        else:
            var=0
            ultratrig=0
            flag=False
    GPIO.cleanup()

def Final_trig():
    while(1):
        if(ultratrig==1 and audiotrig==1):
            #threadLock.acquire()         ---------------------------------------------check
            GPIO.output(LED,True)
            time.sleep(10)
            GPIO.output(LED,False)
            #threadLock.release()

try:
    t1 = Thread(target=audio_check, args=())
    t2 = Thread(target=ultra_check, args=())
    t3 = Thread(target=Final_trig, args=())
    t1.start()
    t2.start()
    t3.start()
except:
    print("Unable to pass thread")
