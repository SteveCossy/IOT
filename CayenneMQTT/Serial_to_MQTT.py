#!/usr/bin/env python
# Major update, Steve Cosgrove, 25 Nov 2019

import cayenne.client, datetime, time, serial, logging, csv, os, requests, datetime, time, glob, uuid, sys, toml

# python3 -m pip install --user pyserial

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
port = serial.Serial(SERIAL_PORT, baudrate=2400)

client = cayenne.client.CayenneMQTTClient()
client.begin(CayenneParam.get('CayUsername'), \
   CayenneParam.get('CayPassword'), \
   CayenneParam.get('CayClientID'), \
   )
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
    header,node,channel,data,csum = rcv.split(",")

    chksum = 0
    for byte in rcv[0:5]:
        chksum = chksum ^ byte
        print(byte, chksum)

    #Test >>> 
    
    print("rcv.split Data = : " + node + " " + channel + " " + data + " " + CrLf)
    headnode = header + node
    if headnode == ':01' and chksum == '0':
    #if cs = Check Sum is good = 0 then do the following
 
            ##This dictionary Holds Key:Value pairs, the Key can be a channel reference
            #DataDict = {'A' : 1, 'B' : 2, 'C' : 3, 'D' : 4, 'E' : 5, 'F' : 6, 'G' : 7, 
            #            'H' : 8, 'I' : 9, 'J' : 10, 'K' : 11, 'L' : 12, 'M' : 13, 'N' : 14, 
            #            'O' : 15, 'P' : 16, 'Q' : 17, 'R' : 18, 'S' : 19, 'T' : 20, 'U' : 21, 
            #            'V' : 22, 'W' : 23, 'X' : 24, 'Y' : 25, 'Z' : 26}
            ##This KeyValue is picked from the dictionary based on the 'channel' variable
            ##and is used as an argument in client.virtualWrite()
            #KeyValue = DataDict[channel]

            client.virtualWrite(channel, data, "analog_sensor", "null")
            client.loop()
      
      #if channel == 'A':
      #  data = float(data)/1
      #  if data < 60000:
      #    client.virtualWrite(1, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'B':
      #  data = float(data)/1
      #  if data < 60000:
      #    client.virtualWrite(2, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'C':
      #  data = float(data)/1
      #  if data < 5000:
      #    client.virtualWrite(3, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'D':
      #  data = float(data)/1
      #  if data < 500:
      #    client.virtualWrite(4, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'E':
      #  data = float(data)/1
      #  if data < 5000:
      #    client.virtualWrite(5, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'F':
      #  data = float(data)/1
      #  if data < 5000:
      #    client.virtualWrite(6, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'G':
      #  data = float(data)/1
      #  if data < 5000:
      #    client.virtualWrite(7, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'H':
      #  data = float(data)/1
      #  if data < 5000:
      #    client.virtualWrite(8, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'I':
      #  data = float(data)/1
      #  if data < 5000:
      #    client.virtualWrite(9, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'J':
      #  data = float(data)/60000
      #  if data < 500:
      #    client.virtualWrite(10, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'K':
      #  data = float(data)/60000
      #  if data < 500:
      #    client.virtualWrite(11, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'L':
      #  data = float(data)/1
      #  if data < 500:
      #    client.virtualWrite(12, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'M':
      #  data = float(data)/1
      #  if data < 500:
      #    client.virtualWrite(13, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'N':
      #  data = float(data)/1
      #  if data < 500:
      #    client.virtualWrite(14, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'O':
      #  data = float(data)/1
      #  if data < 500:
      #    client.virtualWrite(15, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'P':
      #  data = float(data)/1
      #  if data < 500:
      #    client.virtualWrite(16, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'Q':
      #  data = float(data)/1
      #  if data < 500:
      #    client.virtualWrite(17, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'R':
      #  data = float(data)/1
      #  if data < 500:
      #    client.virtualWrite(18, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'S':
      #  data = float(data)/1
      #  if data < 500:
      #    client.virtualWrite(19, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'T':
      #  data = float(data)/1
      #  if data < 500:
      #    client.virtualWrite(20, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'U':
      #  data = float(data)/1
      #  if data < 500:
      #    client.virtualWrite(21, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'V':
      #  data = float(data)/1
      #  if data < 500:
      #    client.virtualWrite(22, data, "analog_sensor", "null")
      #    client.loop()

      #if channel == 'W':
      #  data = float(data)/10
      #  client.virtualWrite(23, data, "analog_sensor", "null")
      #  client.loop()

      #if channel == 'X':
      #  data = float(data)/1
      #  client.virtualWrite(24, data, "analog_sensor", "null")
      #  client.loop()

      #if channel == 'Y':
      #  data = float(data)/1
      #  client.virtualWrite(25, data, "analog_sensor", "null")
      #  client.loop()

      #if channel == 'Z':
      #  data = float(data)/1
      #  client.virtualWrite(26, data, "analog_sensor", "null")
      #  client.loop()

  except ValueError:
    #if Data Packet corrupt or malformed then...
    print("Data Packet corrupt or malformed")

