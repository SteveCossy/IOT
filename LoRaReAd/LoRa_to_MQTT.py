#!/usr/bin/env python
# Read bits direct from LoRa module, Steve Cosgrove, 5 Jan 2020

import cayenne.client, datetime, time, serial, logging, csv, os, requests, datetime, time, glob, uuid, sys, toml, struct

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
#port = serial.Serial(
#    port = SERIAL_PORT,
baudrate=2400
#    parity = serial.PARITY_NONE,
#    stopbits = serial.STOPBITS_ONE,
#    bytesize = serial.EIGHTBITS,
#    )

while True:
   with serial.Serial(SERIAL_PORT, baudrate) as ser:
      PacketIn = ser.read(7)
      print( PacketIn, len(PacketIn) )
      head1,head2,Device,Channel,Data,Cks=struct.unpack("<ccccHB",PacketIn) # Data processing
#      null, null, b8,    b9,  b10,b11,Cks=struct.unpack("<BBBBBBB",PacketIn) # Checksum processing
      CksTest = 0
      for x in range(2,6):
          CksTest = CksTest ^ x
#      for x in [head1,head2,Device,Channel,Data,Cks]:
      print(Data)
      print( 'Calculated data: ',(PacketIn[4] + PacketIn[5] * 256) )
      if CksTest == 0:
          print( 'Checksum correct!')

# client = cayenne.client.CayenneMQTTClient()
# client.begin(CayenneParam.get('CayUsername'), \
#   CayenneParam.get('CayPassword'), \
#   CayenneParam.get('CayClientID'), \
#   )
#   loglevel=logging.INFO)
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883, loglevel=logging.INFO)






