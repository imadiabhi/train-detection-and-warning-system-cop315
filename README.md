# Train Detection and Warning System COP315

We are using a Rapberry Pi, two ultrasonic sensors, USB microphone, Arduino UNO and bluetooth modules for communication.

### Audio detection:

    python3 audio_detect.py
   
This code records sound for six seconds and computes crosscorrelation coefficient with sample recording '**t37.wav**'(\Train-Audio-Samples-Microphone-14.03.2018\t37.wav).
'**correlation coefficient values of various audio samples.xls**' file contains the analysed data from which cut-off '0.65' is being decided. If correlation coefficient is grater than 0.65, it means that the train was present at the time of recording. 

### Obstacle detection:

    python3 Ultrasonic_detect.py

This code continuously checks the distance of obstacle in front of the sensor. Two ultrasonic sensors are kept at 70° so that their waves don't interfere. The circuit diagram of connection of sensor is being shown in '**circuit.jpg**'. The code will trigger LED connected on GPIO pin 25 only when sensor2 detects obstacle under 2 meters after sensor1 detects it. Overall, LED will be on if train is going in a particular direction. 

### Communication:

    B-MasterLink.ino
    B-SlaveLink.ino

Bluetooth communication is used by us temporarily for communicating with warning hooter at some distance from raspberry Pi. Master code is for sending module and Slave code is for the recieving module.

### Audio and Ultrasonic Detection Combined:

    Detection(Aud+Ultrasonic).py

This code continuously and concurrently run audio detection as well as obstacle detection code and maked GPIO pin 25 high when train is detected by both audio and ultrasonic sensing. On connecting raspberry pi pin 25 to master arduino pin 2, signal will be sent by master bluetooth module and it will be recived by slave bluetooth module which will trigger a hooter.
Master arduino+bluetooth --> sender
Slave arduino+bluetooth --> receiver
