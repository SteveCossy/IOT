#!/usr/bin/env python
# Read bits direct from LoRa module, Steve Cosgrove, 5 Jan 2020

import cayenne.client, datetime, time, serial, logging, csv, os, requests, datetime, time, glob, uuid, sys, toml, struct, traceback
from MQTTUtils import Save2Cayenne
from MQTTUtils import Save2CSV
from MQTTUtils import ProcessError
from MQTTUtils import PiSerial
from MQTTUtils import DataError
from gpiozero  import CPUTemperature


# python3 -m pip install --user pyserial

# Useful constants
HOME_DIR = 	os.environ['HOME']
# HOME_DIR =	'/home/pi' # needed to run from CronTab?
AUTH_FILE = 	'cayenneMQTT.txt'
# LOG_DATE =	datetime.datetime.now().strftime("%Y%m%d_%H%M")
LOG_FILE =	'LOG_' + os.path.basename(__file__)
CSV 	= 	'.csv'
CsvTopic = 	'RSSILatLong'
CSVPath =	HOME_DIR # Maybe change later
Eq	= 	' = '
CrLf	= 	'\r\n'
Qt	= 	'"'

# Variables for this script
DRF126x = 	False # must be DRF127x
# DRF126x = 	True
HEADIN = 	b':'b'0'

ConfPathFile = os.path.join(HOME_DIR, AUTH_FILE)

LogPathFile  = os.path.join(CSVPath, LOG_FILE)
logging.basicConfig(filename=LogPathFile, level=logging.DEBUG)
CurrentTime = datetime.datetime.now().isoformat()
logging.debug(CrLf+'***** Starting at: {a}'.format(a=CurrentTime)+' *****' )

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the details should be put into the file listed above.

# Read the Cayenne configuration stuff into a dictionary
ConfigDict = toml.load(ConfPathFile)
CayenneParam = ConfigDict.get('cayenne')
# print (CayenneParam)

# Set up the serial port.
if ('USB0' in PiSerial() ):
    SERIAL_PORT = "/dev/ttyUSB0"
else:
    SERIAL_PORT = "/dev/serial0"

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
SerialListen = True
# Save2Cayenne (client, 'Z', '123>') # Random experiement (didn't work)
try:
 while SerialListen:
   with serial.Serial(SERIAL_PORT, BAUDRATE) as ser:
# Data processing
#      if DRF126x:
#         PacketIn = ser.read(8)
#         head1,head2,Device,Channel,Data,Cks,RSSI=struct.unpack("<ccccHBB",PacketIn)
#      else:
#         PacketIn = ser.read(7)
#         head1,head2,Device,Channel,Data,Cks     =struct.unpack("<ccccHB" ,PacketIn)
#         RSSI = 0
      Sync = ser.read_until(HEADIN)
# debugging      Sync = str(Sync)+"*"
      if not(Sync==HEADIN):
          print( "Extra Sync text!", Sync, "**************")
          Save2Cayenne (client, 'Stat', 1)
          Save2CSV (CSVPath, CayenneParam.get('CayClientID'), 'Sync-Error', Sync)
#      print( "Header read:",Sync )

#      while (len(PacketIn) < 6):
      PacketIn = ser.read(5)
#      print( PacketIn, len(PacketIn), 'l' )

      Device,Channel,Data,Cks=struct.unpack("<ccHB",PacketIn)
      if DRF126x :
          RSSI = ser.read(1)
      else:
          RSSI = 0

#      null, null, b8,    b9,  b10,b11,Cks=struct.unpack("<BBBBBBB",PacketIn) (eg of PicAxe line)
# Checksum processing
      CksTest = 0
#      for byte in PacketIn[2:7]:
      for byte in PacketIn[0:5]:
          CksTest = CksTest ^ byte
#          print(byte, CksTest)
#      print(Cks)
#      for x in [head1,head2,Device,Channel,Data,Cks]:
      print(Device, Channel, Data, Cks, "RSSI = ", RSSI)
#      print( 'Calculated Data: ',(PacketIn[4] + PacketIn[5] * 256) )
      Channel = str(Channel,'ASCII')

      if CksTest == 0:
          print( 'Checksum correct!')
          CPUtemp = CPUTemperature().temperature
          Save2CSV (CSVPath, CayenneParam.get('CayClientID'), Channel, Data) # Send a backup to a CSV file
          Save2Cayenne (client, Channel, Data)
          Save2Cayenne (client, 'V', RSSI)
          Save2Cayenne (client, 'CPUtemp', CPUtemp)
          Save2Cayenne (client, 'Stat', 0) # No errors at this point!
      else:
          print( '"Huston - We have a problem!" *******************************' )
          Save2CSV (CSVPath, CayenneParam.get('CayClientID'), 'Error', PacketIn)
          DataError(Device , Channel, \
              "Checksums (recv/calc): "+str(Cks)+"/"+str(CksTest), PacketIn)
      client.loop()
except:
  Message = 'Exception Reading LoRa Data'
  ProcessError(CSVPath, CayenneParam.get('CayClientID'), \
       client, LOG_FILE, Message)
  SerialListen = False
