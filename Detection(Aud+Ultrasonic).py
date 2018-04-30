import os
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

class trig:
    audiotrig= 0
    ultratrig= 0

    def __init__(self):
        audiotrig= 0
        ultratrig= 0

    def set_audiotrig_up(self):
        self.audiotrig= 1

    def set_audiotrig_down(self):
        self.audiotrig= 0

    def get_audiotrig(self):
        return self.audiotrig

    def set_ultratrig_up(self):
        self.ultratrig= 1

    def set_ultratrig_down(self):
        self.ultratrig= 0

    def get_ultratrig(self):
        return self.ultratrig

def mean2(x):
    y = np.sum(x) / np.size(x);
    return y

def corr2(a,b):
    a = a - mean2(a)
    b = b - mean2(b)
    r = (a*b).sum() / math.sqrt((a*a).sum() * (b*b).sum());
    return r

def audio_check():
    print("audio_check_Starting")
    (rate,t37) = wav.read("37.wav")
    t37 = t37/32767.0    
    t37e = abs(np.fft.fft(t37.T))
    while(1):
        print("start recording")
        os.system("arecord -f cd -D plughw:1,0 -d 6 recorded_sound.wav")
        print("recoring done--processing now")    
        (rate,t) = wav.read("recorded_sound.wav")
        t=t[0:264600]
        t = t/32767.0
        te = abs(np.fft.fft(t.T))
        R1 = corr2(t37e,te)
        print(R1)
        if(R1>0.65 ):
            tr.set_audiotrig_up()
            print("audio_detected")
        else:
            tr.set_audiotrig_down()


def ultra_check():
    print("start ultra_check")
    while(1):
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

        #distance1 = round(distance1, 2)
        #distance2 = round(distance2, 2)
        print(distance1)
        print(distance2)
        if(distance1<200 and distance2>200):
            flag=False
            var=1
            tr.set_ultratrig_down()
        elif(distance1<200 and distance2<200 and var==1):
            tr.set_ultratrig_up()
            time.sleep(5)                    
            flag = True
        else:
            var=0
            tr.set_ultratrig_up()
            flag=False
    GPIO.cleanup()

def Final_trig():
    print("start Final_trig")
    while(1):
        if(tr.get_ultratrig()==1 and tr.get_audiotrig()==1):
            GPIO.output(LED,True)
            time.sleep(10)
            print("TRAIN IS HERE-------------------------")
            GPIO.output(LED,False)
            
tr = trig()

try:
    t1 = Thread(target=audio_check, args=())
    t2 = Thread(target=ultra_check, args=())
    t3 = Thread(target=Final_trig, args=())
    t1.start()
    t2.start()
    t3.start()
except:
    print("Unable to pass thread")
