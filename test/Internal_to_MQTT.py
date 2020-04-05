#!/usr/bin/env python
# Read internal values and send to MQTT, Steve Cosgrove, 5 Jan 2020

import cayenne.client, datetime, time, serial, logging, csv, os, requests, datetime, time, glob, uuid, sys, toml, struct, traceback
from MQTTUtils import Save2Cayenne
from MQTTUtils import Save2CSV
from MQTTUtils import ProcessError
# from MQTTUtils import PiSerial
from MQTTUtils import DataError
from gpiozero  import CPUTemperature


# python3 -m pip install --user pyserial

# Useful constants
HOME_DIR = 	os.environ['HOME']
# HOME_DIR =	'/home/pi'
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
INTERVAL =	10 # Seconds between sending readings

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

SendData = True
# Save2Cayenne (client, 'Z', '123>') # Random experiement (didn't work)
try:
 while SendData:
      timestamp = time.time()
      Channel = 'CPUtemp'
      Data = CPUTemperature().temperature
      Save2CSV (CSVPath, CayenneParam.get('CayClientID'), Channel, Data) # Send a backup to a CSV file
      Save2Cayenne (client, Channel, Data)
      Save2Cayenne (client, 'Stat', 1) # No errors at this point!
      time.sleep(INTERVAL)
      client.loop()
except:
  Message = 'Exception Processing Internal Data'
  ProcessError(CSVPath, CayenneParam.get('CayClientID'), \
       client, LOG_FILE, Message)
