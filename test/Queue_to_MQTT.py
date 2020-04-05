#!/usr/bin/env python
# Read Dicts from Queue then send to MQTT server, Steve Cosgrove, 5 Jan 2020

import cayenne.client, datetime, time, serial, logging, csv, os, requests, datetime, time, glob, uuid, sys, toml, struct, traceback
from MQTTUtils import Save2Cayenne
from MQTTUtils import Save2CSV
from MQTTUtils import ProcessError
from MQTTUtils import PiSerial
from MQTTUtils import DataError
from gpiozero  import CPUTemperature
from persistqueue import Queue


# Useful constants
HOME_DIR = 	os.environ['HOME']
# HOME_DIR =	'/home/pi' # needed to run from CronTab?
AUTH_FILE = 	'cayenneMQTT.txt'
# LOG_DATE =	datetime.datetime.now().strftime("%Y%m%d_%H%M")
LOG_FILE =	'LOG_' + os.path.basename(__file__)
CSV 	= 	'.csv'
CsvTopic = 	'RSSILatLong'
CSVPath =	HOME_DIR # Maybe change later
QUEUE_FILE =	'CayenneQ'

Eq	= 	' = '
CrLf	= 	'\r\n'
Qt	= 	'"'

ConfPathFile = os.path.join(HOME_DIR, AUTH_FILE)
QueuePathFile = os.path.join(CSVPath, QUEUE_FILE)

LogPathFile  = os.path.join(CSVPath, LOG_FILE)
logging.basicConfig(filename=LogPathFile, level=logging.DEBUG)
CurrentTime = datetime.datetime.now().isoformat()
logging.debug(CrLf+'***** Starting at: {a}'.format(a=CurrentTime)+' *****' )

# Read the Cayenne configuration stuff into a dictionary
ConfigDict = toml.load(ConfPathFile)
CayenneParam = ConfigDict.get('cayenne')

ConfPathFile = os.path.join(HOME_DIR, AUTH_FILE)
QueuePathFile = os.path.join(CSVPath, QUEUE_FILE)

LogPathFile  = os.path.join(CSVPath, LOG_FILE)
logging.basicConfig(filename=LogPathFile, level=logging.DEBUG)
CurrentTime = datetime.datetime.now().isoformat()
logging.debug(CrLf+'***** Starting at: {a}'.format(a=CurrentTime)+' *****' )

# Read the Cayenne configuration stuff into a dictionary
ConfigDict = toml.load(ConfPathFile)
CayenneParam = ConfigDict.get('cayenne')

def on_message(client, userData, message):
# based on https://developers.mydevices.com/cayenne/docs/cayenne-mqtt-api/#cayenne-mqtt-api-mqtt-messaging-topics-send-actuator-updated-value
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

CheckingQueue = True

while CheckingQueue:

    CayQueue = Queue(QueuePathFile, autosave=True)

    if not(CayQueue.empty()):
        CayPacket = CayQueue.get()

        Save2CSV (CSVPath, \
            CayPacket['CayClientID'], \
            CayPacket['Channel'], \
            CayPacket['Data'] \
                  ) # Send a backup to a CSV file

        Save2Cayenne (client, \
            CayPacket['Channel'], \
            CayPacket['Data'] \
                  ) # Send 

#        client.loop()
#    CayQueue.task_done()
    time.sleep(1)

