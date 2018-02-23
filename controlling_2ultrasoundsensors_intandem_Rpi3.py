#how to start this code and avoid memory out of bounds in while true

import RPi.GPIO as GPIO
import time
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
while(True):
    GPIO.output(LED,flag)
    GPIO.output(TRIG1,False)
    time.sleep(0.2)
    GPIO.output(TRIG1,True)
    time.sleep(0.00001)
    GPIO.output(TRIG1,False)
    while GPIO.input(ECHO1)==0:
        pulse_start1 = time.time()
    while GPIO.input(ECHO1)==1:
        pulse_end1 = time.time()
    pulse_duration1 = pulse_end1 - pulse_start1

    GPIO.output(TRIG2,False)
    time.sleep(0.2)
    GPIO.output(TRIG2,True)
    time.sleep(0.00001)
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
    if(distance1<20 and distance2>20):
        flag=False
        var=1
    elif(distance1<20 and distance2<20 and var==1):
        GPIO.output(LED,True)
        print("LED ON")
        flag = True
    else:
        var=0
        flag=False
GPIO.cleanup()
