#!/usr/bin/env python
# Major update, Steve Cosgrove, 25 Nov 2019

import cayenne.client, datetime, time, serial, logging, csv, os, requests, datetime, time, glob, uuid, sys, toml

# Useful constants
HomeDir = 	os.environ['HOME']
# HomeDir	= '/home/pi'
ConfFile = '/cayenneMQTT.txt'
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
#  and the details should be put into the file listed above.

# Read the Cayenne configuration stuff into a dictionary
ConfigDict = toml.load(ConfPathFile)
CayenneParam = ConfigDict.get('cayenne')
print (CayenneParam)

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

#This sets up the serial port specified above. baud rate is the bits per second timeout seconds
#port = serial.Serial(SERIAL_PORT, baudrate=2400, timeout=5)

#This sets up the serial port specified above. baud rate and WAITS for any cr/lf (new blob of data from picaxe)
port = serial.serial(SERIAL_PORT, baudrate=2400)

client = cayenne.client.CayenneMQTTClient()
client.begin(CayenneParam.get('CayUsername'), \
   CayenneParam.get('CayPassword'), \
   CayenneParam.get('CayClientID'), \
   loglevel=logging.INFO)
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883, loglevel=logging.INFO)

error=123

while True:
  try:
    rcv = port.readline() #read buffer until cr/lf
    #Test >>> print("Serial Readline Data = " + rcv)
    rcv = rcv.rstrip("\r\n")
    node,channel,data,cs = rcv.split(",")
    #Test >>> print("rcv.split Data = : " + node + " " + channel + " " + data + " " + cs)
    if node == ':01' and cs == '0':
    #if cs = Check Sum is good = 0 then do the following
 
      if channel == 'A':
        data = float(data)/1
        if data < 60000:
          client.virtualWrite(1, data, "analog_sensor", "null")
          client.loop()

      if channel == 'B':
        data = float(data)/1
        if data < 60000:
          client.virtualWrite(2, data, "analog_sensor", "null")
          client.loop()

      if channel == 'C':
        data = float(data)/1
        if data < 5000:
          client.virtualWrite(3, data, "analog_sensor", "null")
          client.loop()

      if channel == 'D':
        data = float(data)/1
        if data < 500:
          client.virtualWrite(4, data, "analog_sensor", "null")
          client.loop()

      if channel == 'E':
        data = float(data)/1
        if data < 5000:
          client.virtualWrite(5, data, "analog_sensor", "null")
          client.loop()

      if channel == 'F':
        data = float(data)/1
        if data < 5000:
          client.virtualWrite(6, data, "analog_sensor", "null")
          client.loop()

      if channel == 'G':
        data = float(data)/1
        if data < 5000:
          client.virtualWrite(7, data, "analog_sensor", "null")
          client.loop()

      if channel == 'H':
        data = float(data)/1
        if data < 5000:
          client.virtualWrite(8, data, "analog_sensor", "null")
          client.loop()

      if channel == 'I':
        data = float(data)/1
        if data < 5000:
          client.virtualWrite(9, data, "analog_sensor", "null")
          client.loop()

      if channel == 'J':
        data = float(data)/60000
        if data < 500:
          client.virtualWrite(10, data, "analog_sensor", "null")
          client.loop()

      if channel == 'K':
        data = float(data)/60000
        if data < 500:
          client.virtualWrite(11, data, "analog_sensor", "null")
          client.loop()

      if channel == 'L':
        data = float(data)/1
        if data < 500:
          client.virtualWrite(12, data, "analog_sensor", "null")
          client.loop()

      if channel == 'M':
        data = float(data)/1
        if data < 500:
          client.virtualWrite(13, data, "analog_sensor", "null")
          client.loop()

      if channel == 'N':
        data = float(data)/1
        if data < 500:
          client.virtualWrite(14, data, "analog_sensor", "null")
          client.loop()

      if channel == 'O':
        data = float(data)/1
        if data < 500:
          client.virtualWrite(15, data, "analog_sensor", "null")
          client.loop()

      if channel == 'P':
        data = float(data)/1
        if data < 500:
          client.virtualWrite(16, data, "analog_sensor", "null")
          client.loop()

      if channel == 'Q':
        data = float(data)/1
        if data < 500:
          client.virtualWrite(17, data, "analog_sensor", "null")
          client.loop()

      if channel == 'R':
        data = float(data)/1
        if data < 500:
          client.virtualWrite(18, data, "analog_sensor", "null")
          client.loop()

      if channel == 'S':
        data = float(data)/1
        if data < 500:
          client.virtualWrite(19, data, "analog_sensor", "null")
          client.loop()

      if channel == 'T':
        data = float(data)/1
        if data < 500:
          client.virtualWrite(20, data, "analog_sensor", "null")
          client.loop()

      if channel == 'U':
        data = float(data)/1
        if data < 500:
          client.virtualWrite(21, data, "analog_sensor", "null")
          client.loop()

      if channel == 'V':
        data = float(data)/1
        if data < 500:
          client.virtualWrite(22, data, "analog_sensor", "null")
          client.loop()

      if channel == 'W':
        data = float(data)/10
        client.virtualWrite(23, data, "analog_sensor", "null")
        client.loop()

      if channel == 'X':
        data = float(data)/1
        client.virtualWrite(24, data, "analog_sensor", "null")
        client.loop()

      if channel == 'Y':
        data = float(data)/1
        client.virtualWrite(25, data, "analog_sensor", "null")
        client.loop()

      if channel == 'Z':
        data = float(data)/1
        client.virtualWrite(26, data, "analog_sensor", "null")
        client.loop()

  except ValueError:
    #if Data Packet corrupt or malformed then...
    print("Data Packet corrupt or malformed")

