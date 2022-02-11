#!/usr/bin/env python
# Major update, Steve Cosgrove, 25 Nov 2019

import string
import cayenne.client, time, serial, logging, csv, os, requests, time, glob, uuid, sys, toml
from datetime import date
from InitializeConfigFile import WriteFile
from DetectionAlgorithms import DetectPeng, DetectErr, GetErrorCount, GetPrevTemp, GetIsPeng, ResetIsPeng
from UsefulConstants import ReturnDict

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
LastCheckFile = date.today()

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
DivisorDict = ConfigDict.get('ChannelDivisors')

# Create Dictionary to store offset values
OffsetDict = ConfigDict.get('OffsetValues')

#This sets up the serial port specified above. baud rate is the bits per second timeout seconds
#port = serial.Serial(SERIAL_PORT, baudrate=2400, timeout=5)

#This sets up the serial port specified above. baud rate and WAITS for any cr/lf (new blob of data from picaxe)
port = serial.Serial(SERIAL_PORT, baudrate=2400)

client = cayenne.client.CayenneMQTTClient()
client.begin(MQTTCreds.get('CayUsername'), \
   MQTTCreds.get('CayPassword'), \
   MQTTCreds.get('CayClientID'))

LastCheckPeng = time.time()

#   loglevel=logging.INFO)
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883, loglevel=logging.INFO)

error=123

while True:
    try:
        # The file compares the date when the file was last checked
        if date.today() > LastCheckFile:
            # if the file hasn't been check today, the file will be reloaded into the variables
            ConfigDict = toml.load(ConfPathFile)
            Thresholds = ConfigDict.get('DetectionThresholds')
            DivisorDict = ConfigDict.get('ChannelDivisors')
            OffsetDict = ConfigDict.get('OffsetValues')
            LastCheckFile = date.today()

        rcv = port.readline() # read buffer until cr/lf
        # Test >>> print("Serial Readline Data = " + str(rcv))
        rcv=rcv.decode("utf-8") # buffer read is 'bytes' in Python 3.x    node,channel,data,cs = rcv.split(",")
        rcv = str(rcv.rstrip("\r\n"))
        receivedData = [int(x) for x in rcv.split(',') if x.strip().isdigit()]
        node, channel, data, chksum = receivedData
    
        channelstr = 'Channel' + str(channel)

        # data is divided here to render the data useable before passing it to the algorithms
        data = float(data) / int(DivisorDict[channelstr]) # finds the required channel divisor in the dict
        print(DivisorDict[channelstr])
        chksum = receivedData[3]
        chkstest = 0 
  
        # chkstest = sum(receivedData[:end])
        # The current implementation of the check takes the sum of the node, channel, and data variables
        # Then subtract the chksum variable, wehich is received from the Cicadacom module

        chkstest = int(node) + int(channel) + int(data)

        #Test >>> 
        # chkstest = chkstest - chksum
        print('chkstest = ', chkstest, ', chksum = ', chksum)

        print('channel = ', channel)

        # Check if time has passed to reset the Peng            
        print(time.time() - LastCheckPeng)
        if (time.time() - LastCheckPeng) >= 300:
            ResetIsPeng()
            LastCheckPeng = time.time()

        #print("rcv.split Data = : " + node + " " + channel + " " + data + " " + CrLf)
        print (receivedData)
        if chkstest == chksum:
        #if cs = Check Sum is good = 0 then do the following
            print('Checksum okay, sending to Cayenne')
            QosGood += 1

            if OffsetDict:
                Offset = int(OffsetDict['Offset' + str(channel)])
                print('offset = ', Offset)
                data = data + Offset

            if channel % 5 and channel != 26: # Each 5th channel is used to monitor mA, they shouldn't be used for temperature testing
                print('data = ', data)
                # print functions for debugging
                print('Running detection algorithms')

                # Passes the data to error detection algorithm
                IsError = DetectErr(data, Thresholds['ErrThresh'])
                if IsError != 0:
                    data = GetPrevTemp()
                    print(data)
                
                # publishes the current number of errors to Cayenne
                ErrorCount = GetErrorCount()
                print('ErrCount = ', ErrorCount)
                client.virtualWrite(49, ErrorCount, "analog_sensor", "null")
                
                # Passes the data to the penguin detection algorithm
                if GetIsPeng() == 0:
                    IsPeng = DetectPeng(data, Thresholds['DetectThresh'])
                    print('IsPeng = ', IsPeng)
                    client.virtualWrite(48, IsPeng, "digital_sensor", "null")

            client.virtualWrite(channel, data, "analog_sensor", "null")
            client.loop()
        else:
            QosBad += 1
            print('Bad checksum')

        #if QosBad >= 1 and QosGood >= 1:
        #    Qos = QosGood / QosBad
        #    client.virtualWrite(<enter channel number>, Qos, "analog_sensor", "null")

    except ValueError:
        # if Data Packet corrupt or malformed then...
        QosBad += 1
        print("Data Packet corrupt or malformed")