#!/usr/bin/env python
# Read bits direct from LoRa module, Steve Cosgrove, 5 Jan 2020

import os, logging, datetime

# Logging file creation was moved to the top of the code for bug fixing/troubleshooting purposes
HomeDir = 	os.environ['HOME']
CSVPath =	os.path.join(HomeDir, 'CSVdata')
LOG_FILE =	'LOG_' + os.path.basename(__file__)
CrLf	= 	'\r\n'

LogPathFile  = os.path.join(CSVPath, LOG_FILE)
logging.basicConfig(filename=LogPathFile, level=logging.DEBUG, force=True)
CurrentTime = datetime.datetime.now().isoformat()
logging.debug(CrLf+'***** Starting at: {a}'.format(a=CurrentTime)+' *****' )

from pickle import TRUE
import cayenne.client, time, serial, csv,  requests, datetime, time, glob, uuid, sys, toml, struct, traceback, string
from MQTTUtils import Save2Cayenne
from MQTTUtils import Save2CSV
# from MQTTUtils import ProcessError # This function has been moved out of the library where it didn't work as expected.
from MQTTUtils import PiSerial
from MQTTUtils import DataError
from SensorLib import ReadTemp
from SensorLib import DetectPeng
from SensorLib import GetErrCount
from InitializeConfigFile import WriteFile
from gpiozero import CPUTemperature


# python3 -m pip install --user pyserial

# Useful constants
CONF_FILE = 	'MQTTConfig.txt'
# LOG_DATE =	datetime.datetime.now().strftime("%Y%m%d_%H%M")
CSV 	= 	'.csv'
CsvTopic = 	'RSSILatLong'
Eq	= 	' = '
Qt	= 	'"'

# Variables for this script
DRF126x = 	False # must be DRF127x
# DRF126x = 	True
HEADIN = 	b':'b'0'

#   Define the PicAxe Divisors
DivisorDict = dict.fromkeys(string.ascii_uppercase)
#for key in DivisorDict :
#    DivisorDict[key] =	1
#DivisorDict['A'] =	10 # Soil Moisture
#DivisorDict['B'] =	10 # Temperature
## The following values are based on the table found on the wiki.
## Found at https://github.com/SteveCossy/IOT/wiki/Tables-defining:-Cayenne-Data-Channels---PicAxe-Channels---Cicadacom
#DivisorDict['H'] =  60000
#DivisorDict['J'] =  60000
#DivisorDict['K'] =  256

ConfPathFile = os.path.join(HomeDir, CONF_FILE)

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the details should be put into the file listed above.

File = os.path.isfile(ConfPathFile)
# Checking if the file is present
if File == False:
#   create create file using script

   MQTTUser = input('Paste MQTT Username')

   MQTTPass = input('Paste MQTT Password')

   ClientID = input('Paste Unique Client ID')

#  call function here (MQTTUser, MQTTPass, ClientID)
   WriteFile(MQTTUser, MQTTPass, ClientID)


# Read the Cayenne configuration stuff into a dictionary
# Loads the config
ConfigDict = toml.load(ConfPathFile)
MQTTCreds = ConfigDict.get('MQTTCredentials')
# print (CayenneParam)

# Create dictionary to store channel divisors
DivisorDict[]
i=1
while i <= 26:
    DivisorDict[str(i)] = 1
    i += 1

# Changes the values for some channels that require non-standard divisors
# These are based on the divisors from the original if statements
ChannelDivs = ConfigDict.get('ChannelDivisors')
DivisorDict['Channel10'] = ChannelDivs.get('Channel10')
DivisorDict['Channel11'] = ChannelDivs.get('Channel11')
DivisorDict['Channel23'] = ChannelDivs.get('Channel23')

# Set up the serial port.
if ('USB0' in PiSerial() ):
    SERIAL_PORT = "/dev/ttyUSB0"
else:
    SERIAL_PORT = "/dev/serial0"
#    SERIAL_PORT =  "/dev/ttyAMA0"
# Default location of serial port on Pi models 3 and Zero
#    SERIAL_PORT =   "/dev/ttyS0"

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

def ProcessError(CSVPath, ClientID, CayClient, CSV_Message, Message):
# Save Message to a file and Cayenne
    global LastError
    CurrentTime = datetime.datetime.now().isoformat()
    CSVPathFile = Save2CSV (CSVPath, ClientID, 'Exception', CSV_Message)
    CurrentTime = datetime.datetime.now().isoformat()
    LogPathFile = logging.getLoggerClass().root.handlers[0].baseFilename

# Connect to Cayenne Cloud
client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.on_connect = on_connect

client.begin(MQTTCreds.get('MQTTUsername'), \
   MQTTCreds.get('MQTTPassWord'), \
   MQTTCreds.get('MQTTClientID'), \
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
          Save2Cayenne (client, 'Stat', 1, 1)
          Save2CSV (CSVPath, MQTTCreds.get('Client ID'), 'Sync-Error', Sync)
#      print( "Header read:",Sync )

#      while (len(PacketIn) < 6):
      PacketIn = ser.read(5)
      print( PacketIn, len(PacketIn), 'l' )

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
          ExtTemp = ReadTemp()
          PengDetect = DetectPeng()
          ErrCount = GetErrCount()
          Save2CSV (CSVPath, MQTTCreds.get('MQTTClientID'), Channel, Data) # Send a backup to a CSV file
          Save2Cayenne (client, Channel, Data, DivisorDict[Channel])
          Save2Cayenne (client, 'V', RSSI, 1)
          Save2Cayenne (client, 'CPUtemp', CPUtemp, 1)
          Save2Cayenne (client, 'ExtTemp', ExtTemp, 1)
          Save2Cayenne (client, 'Stat', 0, 1) # No errors at this point!
          Save2Cayenne (client, 'PengDetect', PengDetect, 1)
          Save2Cayenne (client, 'ErrCount', ErrCount, 1)
      else:
          print( '"Huston - We have a problem!" *******************************' )
          Save2CSV (CSVPath, MQTTCreds.get('MQTTClientID'), 'Error', PacketIn)
          DataError(Device , Channel, \
              "Checksums (recv/calc): "+str(Cks)+"/"+str(CksTest), PacketIn)
   client.loop()
except KeyboardInterrupt:
  print(' ')

except:
  Message = 'Exception Reading LoRa Data'
  ProcessError(CSVPath, MQTTCreds.get('MQTTClientID'), \
       client, LOG_FILE, Message)

# SerialListen = False
print('\n','Exiting app') # Send a cheery message
time.sleep(4)           # Four seconds to allow sending to finish
# client.disconnect()     # Disconnect from broker - Doesn't work with Cayenne libraies
# client.loop_stop()      # Stop looking for messages