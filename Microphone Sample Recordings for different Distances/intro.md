//The different sample recordings of Microphone, after connecting from Raspberry Pi are saved here.

//To see the attached Audio Devices:

arecord –l

**** List of CAPTURE Hardware Devices ****

card 0: Device [USB PnP Sound Device], device 0: USB Audio [USB Audio]

  Subdevices: 1/1
  
  Subdevice #0: subdevice #0
  
//To start recording for 20s and save changes in test.wav

$ arecord -f cd -D plughw:1,0 -d 20 test.wav
