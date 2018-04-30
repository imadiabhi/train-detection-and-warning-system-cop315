import scipy.io.wavfile as wav
import numpy as np
import math
import os

def mean2(x):
    y = np.sum(x) / np.size(x);
    return y

def corr2(a,b):
    a = a - mean2(a)
    b = b - mean2(b)
    r = (a*b).sum() / math.sqrt((a*a).sum() * (b*b).sum());
    return r

os.system("arecord -f cd -D plughw:1,0 -d 6 recorded_sound.wav")   #recording
(rate,t37) = wav.read("37.wav")                                    #storing in a matrix  
(rate,t) = wav.read("recorded_sound.wav")
t = t[0:264600]
t37 = t37/32767.0
t = t/32767.0
t37e = abs(np.fft.fft(t37.T))                                      #taking fast fourier transform
t = abs(np.fft.fft(t.T))
R = corr2(t37e,t19e)                                               #computing correlation coefficient
if(R>0.65):
	print("Train is Here")
