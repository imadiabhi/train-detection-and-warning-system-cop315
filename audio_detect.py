import scipy.io.wavfile as wav
import numpy as np
import math

def mean2(x):
    y = np.sum(x) / np.size(x);
    return y

def corr2(a,b):
    a = a - mean2(a)
    b = b - mean2(b)
    r = (a*b).sum() / math.sqrt((a*a).sum() * (b*b).sum());
    return r

(rate,t37) = wav.read("37.wav")
(rate,t19) = wav.read("19.wav")
t37 = t37/32767.0
t19 = t19/32767.0
t37e = abs(np.fft.fft(t37.T))
t19e = abs(np.fft.fft(t19.T))
R = corr2(t37e,t19e)
if(R>0.65):
	print("Train is Here")