import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIG1=23
ECHO1=24
LED=25
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)
flag = False
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
    distance1 = pulse_duration1 * 17150
    distance1 = round(distance1, 2)
    print(distance1)
    if(distance1<20):
        GPIO.output(LED,True)
        flag = True
    else:
        flag=False
GPIO.cleanup()
