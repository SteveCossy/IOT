from MQTTUtils import PiSerial

serialDevices = PiSerial()

print('Onboard port is:'+serialDevices['Onboard'] )
print('USB port(s):',end='')
for Device in serialDevices.keys() :
    if 'USB' in Device:
       print(Device,end=',')
print()

