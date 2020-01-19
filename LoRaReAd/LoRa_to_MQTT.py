#!/usr/bin/env python
# Read bits direct from LoRa module, Steve Cosgrove, 5 Jan 2020

import cayenne.client, datetime, time, serial, logging, csv, os, requests, datetime, time, glob, uuid, sys, toml, struct
from MQTTUtils import Save2Cayenne
from MQTTUtils import Save2CSV

# python3 -m pip install --user pyserial

# Useful constants
HOME_DIR = 	os.environ['HOME']
# HOME_DIR =	'/home/pi'
AUTH_FILE = 	'cayenneMQTT.txt'
CSV 	= 	'.csv'
CsvTopic = 	'RSSILatLong'
CSVPath =	HOME_DIR # Maybe change later
Eq	= 	' = '
CrLf	= 	'\r\n'
Qt	= 	'"'

def DataError(Device, Channel, textMessage, PacketIn):
    print ("Device: ",Device,CrLf \
        ,"Channel: ",Channel,CrLf \
        ,"Message: ",textMessage,CrLf \
        ,"Packet Recieved: '"+str(PacketIn)+"'" \
        )


ConfPathFile = os.path.join(HOME_DIR, AUTH_FILE)

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

# Set up the serial port.
# Default location of serial port on pre 3 Pi models
# SERIAL_PORT =  "/dev/ttyAMA0"
# Default location of serial port on Pi models 3 and Zero
SERIAL_PORT =   "/dev/ttyS0"
BAUDRATE=2400
# These values appear to be the defaults
#    parity = serial.PARITY_NONE,
#    stopbits = serial.STOPBITS_ONE,
#    bytesize = serial.EIGHTBITS,

# The callback for when a message is received from Cayenne.
def on_message(client, userData, message):
# based on https://developers.mydevices.com/cayenne/docs/cayenne-mqtt-api/#cayenne-mqtt-api-mqtt-messaging-topics-send-actuator-updated-value
#    global COUNTER
    print("message received: " ,str(message.payload.decode("utf-8")))

def on_connect(client, userData, flags, rc):
    print("Connected with result code "+str(rc))

# Connect to Cayenne Cloud
client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.on_connect = on_connect

client.begin(CayenneParam.get('CayUsername'), \
   CayenneParam.get('CayPassword'), \
   CayenneParam.get('CayClientID'), \
   )
#   loglevel=logging.INFO)  # Logging doesn't seem to work in Python3
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883, loglevel=logging.INFO)

while True:
   with serial.Serial(SERIAL_PORT, BAUDRATE) as ser:
      PacketIn = ser.read(8)
      print( PacketIn, len(PacketIn) )
# Data processing
      head1,head2,Device,Channel,Data,Cks,RSSI=struct.unpack("<ccccHBB",PacketIn)
      Channel = str(Channel,'ASCII')
#      null, null, b8,    b9,  b10,b11,Cks=struct.unpack("<BBBBBBB",PacketIn) 
# Checksum processing
      CksTest = 0
      for byte in PacketIn[2:7]:
          CksTest = CksTest ^ byte
#          print(byte, CksTest)
#      for x in [head1,head2,Device,Channel,Data,Cks]:
      print(Device, Channel, Data, Cks, "RSSI = ", RSSI)
#      print( 'Calculated Data: ',(PacketIn[4] + PacketIn[5] * 256) )
      if CksTest == 0:
          print( 'Checksum correct!')
          Save2CSV (CSVPath, CayenneParam.get('CayClientID'), Channel, Data) # Send a backup to a CSV file
          Save2Cayenne (client, Channel, Data)
      else:
          print( '"Huston - We have a problem!" *******************************' )
          Save2CSV (CSVPath, CayenneParam.get('CayClientID'), 'Error', PacketIn)
          DataError(Device , Channel, \
              "Checksums (recv/calc): "+str(Cks)+"/"+str(CksTest), PacketIn)
      client.loop()


