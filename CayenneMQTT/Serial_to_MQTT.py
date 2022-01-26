#!/usr/bin/env python
# Major update, Steve Cosgrove, 25 Nov 2019

import string
import cayenne.client, datetime, time, serial, logging, csv, os, requests, datetime, time, glob, uuid, sys, toml
from InitializeConfigFile import WriteFile

# python3 -m pip install --user pyserial

# Useful constants
HomeDir = 	os.environ['HOME']
# HomeDir	= '/home/pi'
ConfFile = '/cayenneMQTTConfig.txt'
CsvPath = HomeDir+'/'
CSV 	= '.csv'
CrLf 	= '\r\n'
CsvTopic = 'RSSILatLong'
Eq	= ' = '
CrLf	= '\r\n'
Qt	= '"'

ConfPathFile = HomeDir+ConfFile

# How often shall we write values to Cayenne? (Seconds + 1)
Interval =      60

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the program should write it to the file above.

FileCheck = os.path.isfile(ConfPathFile)

if FileCheck == False:
    MQTTUser = input('Paste MQTT Username')

    MQTTPass = input('Paste MQTT Password')

    ClientID = input('Paste Unique Client ID')

#  call function here (MQTTUser, MQTTPass, ClientID)
    WriteFile(MQTTUser, MQTTPass, ClientID)
    print('File created at ' + ConfPathFile)

# Read the Cayenne configuration stuff into a dictionary
ConfigDict = toml.load(ConfPathFile)
MQTTCreds = ConfigDict.get('MQTTCredentials')
print (MQTTCreds)

# Expected config
# [cayenne]
# CayUsername
# CayPassword
# CayClientID
# UniqueID

# Default location of serial port on pre 3 Pi models
#SERIAL_PORT =  "/dev/ttyAMA0"

# Default location of serial port on Pi models 3 and Zero
SERIAL_PORT =   "/dev/ttyS0"

# Create dictionary to store channel divisors
i = 1
while i <= 26:
    Key = 'Channel' + str(i)
    # The standard divisor is 1
    DivisorDict = dict.fromkeys(Key, 1)

# Changes the values for some channels that require non-standard divisors
ChannelDivs = ConfigDict.get('ChannelDivisors')
DivisorDict['Channel10'] = ChannelDivs.get('Channel10')
DivisorDict['Channel11'] = ChannelDivs.get('Channel11')
DivisorDict['Channel23'] = ChannelDivs.get('Channel23')

#This sets up the serial port specified above. baud rate is the bits per second timeout seconds
#port = serial.Serial(SERIAL_PORT, baudrate=2400, timeout=5)

#This sets up the serial port specified above. baud rate and WAITS for any cr/lf (new blob of data from picaxe)
port = serial.Serial(SERIAL_PORT, baudrate=2400)

client = cayenne.client.CayenneMQTTClient()
client.begin(MQTTCreds.get('CayUsername'), \
   MQTTCreds.get('CayPassword'), \
   MQTTCreds.get('CayClientID'))

#   loglevel=logging.INFO)
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883, loglevel=logging.INFO)

error=123

while True:
  try:
    rcv = port.readline() #read buffer until cr/lf
#    Test >>> print("Serial Readline Data = " + str(rcv))
    rcv=rcv.decode("utf-8") #buffer read is 'bytes' in Python 3.x    node,channel,data,cs = rcv.split(",")
    rcv = str(rcv.rstrip("\r\n"))
    receivedData = [int(x) for x in rcv.split(',') if x.strip().isdigit()]
    channel, data = receivedData[1:3]
    
    channelstr = 'Channel' + str(channel)

    end = len(receivedData) - 1

    chksum = receivedData[end]
    chkstest = 0 

    # chkstest = sum(receivedData[:end])
    # The current implementation of the check takes the sum of the node, channel, and data variables
    # Then subtract the chksum variable, wehich is received from the Cicadacom module

    for byte in receivedData[:end]:
        chkstest = chkstest ^ byte

    #Test >>> 
    # chkstest = chkstest - chksum
    print(chkstest, chksum)

    #print("rcv.split Data = : " + node + " " + channel + " " + data + " " + CrLf)
    print (receivedData)
    if chkstest == 0:
    #if cs = Check Sum is good = 0 then do the following

            print('channel = ', channel, ',  data = ', data)
            data = float(data) / DivisorDict[channelstr] # finds the required channel divisor in the dict
            client.virtualWrite(channel, data, "analog_sensor", "null")
            client.loop()

  except ValueError:
    #if Data Packet corrupt or malformed then...
    print("Data Packet corrupt or malformed")