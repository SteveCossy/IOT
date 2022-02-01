#!/usr/bin/env python
# Major update, Steve Cosgrove, 25 Nov 2019

import string
from CayenneMQTT.DetectionAlgorithms import ErrorCount
from CayenneMQTT.UsefulConstants import ReturnDict
import cayenne.client, datetime, time, serial, logging, csv, os, requests, datetime, time, glob, uuid, sys, toml
from InitializeConfigFile import WriteFile
from DetectionAlgorithms import DetectPeng, DetectErr, GetErrorCount, GetPrevTemp, GetIsPeng, ResetIsPeng

# python3 -m pip install --user pyserial

# Useful constants
#HomeDir = 	os.environ['HOME']
## HomeDir	= '/home/pi'
#ConfFile = '/MQTTConfig.txt'
#CsvPath = HomeDir+'/'
#CSV 	= '.csv'
#CrLf 	= '\r\n'
#CsvTopic = 'RSSILatLong'
#Eq	= ' = '
#Qt	= '"'

ConstantsDict = ReturnDict()

# Variables used to track quality of service
# If a checksum fails or a data packet is unreadble, the QosBad increments, successful checksums increment QosGood
QosBad  = 0
QosGood = 0

ConfPathFile = ConstantsDict['HomeDir']+ ConstantsDict['ConfFile']

# How often shall we write values to Cayenne? (Seconds + 1)
Interval =      60

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the program should write it to the file above.

FileCheck = os.path.isfile(ConfPathFile)

if FileCheck == False:
    MQTTUser = input('Paste MQTT Username: ')

    MQTTPass = input('Paste MQTT Password: ')

    ClientID = input('Paste Unique Client ID: ')

#  call function here (MQTTUser, MQTTPass, ClientID)
    WriteFile(MQTTUser, MQTTPass, ClientID)
    print('File created at ' + ConfPathFile)

# Read the Cayenne configuration stuff into a dictionary
ConfigDict = toml.load(ConfPathFile)
MQTTCreds = ConfigDict.get('MQTTCredentials')
print (MQTTCreds)

Thresholds = ConfigDict.get('DetectionThresholds')
# Might need to create a separate file with the detection algorithms

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
DivisorDict = {}
i=1
while i <= 26:
    DivisorDict['Channel' + str(i)] = '10'
    i += 1

OffsetDict = ConfigDict.get('OffsetValues')

# Changes the values for some channels that require non-standard divisors
# ChannelDivs = ConfigDict.get('ChannelDivisors')

#This sets up the serial port specified above. baud rate is the bits per second timeout seconds
#port = serial.Serial(SERIAL_PORT, baudrate=2400, timeout=5)

#This sets up the serial port specified above. baud rate and WAITS for any cr/lf (new blob of data from picaxe)
port = serial.Serial(SERIAL_PORT, baudrate=2400)

client = cayenne.client.CayenneMQTTClient()
client.begin(MQTTCreds.get('CayUsername'), \
   MQTTCreds.get('CayPassword'), \
   MQTTCreds.get('CayClientID'))

Lastchecked = time.time()

#   loglevel=logging.INFO)
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883, loglevel=logging.INFO)

error=123

while True:
    try:
        rcv = port.readline() #read buffer until cr/lf
        # Test >>> print("Serial Readline Data = " + str(rcv))
        rcv=rcv.decode("utf-8") #buffer read is 'bytes' in Python 3.x    node,channel,data,cs = rcv.split(",")
        rcv = str(rcv.rstrip("\r\n"))
        receivedData = [int(x) for x in rcv.split(',') if x.strip().isdigit()]
        channel, data, chksum = receivedData[1:]
    
        channelstr = 'Channel' + str(channel)

        chksum = receivedData[3]
        chkstest = 0 
  
        # chkstest = sum(receivedData[:end])
        # The current implementation of the check takes the sum of the node, channel, and data variables
        # Then subtract the chksum variable, wehich is received from the Cicadacom module

        chkstest = sum(receivedData[:3])

        #Test >>> 
        # chkstest = chkstest - chksum
        print('chkstest = ', chkstest, ', chksum = ', chksum)

        print('channel = ', channel)

        # Check if time has passed to reset the Peng
        if (time.time() - Lastchecked) >= 300:
            print(time.time() - Lastchecked)
            ResetIsPeng()
            Lastchecked = time.time()

        #print("rcv.split Data = : " + node + " " + channel + " " + data + " " + CrLf)
        print (receivedData)
        if chkstest == 0:
        #if cs = Check Sum is good = 0 then do the following
            print('Checksum okay, sending to Cayenne')
            QosGood += 1

            if len(OffsetDict) > 0:
                Offset = OffsetDict['Offset' + str(channel)]
                print('offset = ', Offset)
                data = data + Offset

            if channel == 2: # channel 2 appears to the channel used for temperature readings
                print('data = ', data)
                # it is done here to render the data useable before p[assing it to the algorithms
                print('Running detection algorithms')

                IsError = DetectErr(data, Thresholds['ErrThresh'])
                if IsError != 0:
                    data = GetPrevTemp()
                    print(data)
                
                ErrCount = GetErrorCount()
                print('ErrCount = ', ErrCount)
                client.virtualWrite(49, ErrorCount, "analog_sensor", "nulkl")
                
                if GetIsPeng() == 0:
                    IsPeng = DetectPeng(data, Thresholds['DetectThresh'])
                    print('IsPeng = ', IsPeng)
                    client.virtualWrite(48, IsPeng, "digital_sensor", "null")

            data = float(data) / int(DivisorDict[channelstr]) # finds the required channel divisor in the dict
            client.virtualWrite(channel, data, "analog_sensor", "null")
            client.loop()
        else:
            QosBad += 1
            print('Bad checksum')

    except ValueError:
        # if Data Packet corrupt or malformed then...
        QosBad += 1
        print("Data Packet corrupt or malformed")