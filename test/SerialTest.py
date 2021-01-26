import os, sys

HomeDir =       os.environ['HOME']
# the IOT/LoRaReAd dir contains MQTTUtils.py
MQTTUpath =     os.path.join(HomeDir,'IOT/LoRaReAd')
sys.path.append(MQTTUpath)
from MQTTUtils import PiSerial

serialDevices = PiSerial()

# print('Onboard port is:'+serialDevices['Onboard'] )
print('USB port(s):',end='')
for Device in serialDevices.keys() :
#    if 'USB' in Device:
       print(Device,end=',')
print()

