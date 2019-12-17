#!/usr/bin/env python
# Major update, Steve Cosgrove, 25 Nov 2019

import cayenne.client, datetime, time, logging, csv, os, requests, datetime, time, glob, uuid, sys, toml

# python3 -m pip install --user pyserial

# Useful constants
HomeDir = 	os.environ['HOME']
# HomeDir	= '/home/pi'
ConfFile = '/testMQTT.txt'
CsvPath = HomeDir+'/'
CSV 	= '.csv'
CrLf 	= '\r\n'
CsvTopic = 'RSSILatLong'
Eq	= ' = '
CrLf	= '\r\n'
Qt	= '"'

CHANNELpub = 15
CHANNELsub = 12
ConfPathFile = HomeDir+ConfFile
INPUTFILE = "RSSILatLong-20191209-Zealandia-ZIP.csv"

COUNTER=[-41.29838,174.74505,100]

# How often shall we write values to Cayenne? (Seconds + 1)
Interval =      10

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

Subscribe       ="v1/{}/things/{}/data/#".format( \
        CayenneParam.get('CayUsername'), \
        CayenneParam.get('CayClientID') )
# The subscribe string we  will send to Cayenne


def on_message(client, userdata, msg):
    print(msg.topic +"&"+ str(msg.payload))
    if "data" in str(msg.topic):
    # test just in case we get a message that is not data (I wonder what we should do with it?)
# eg msg: v1/6375a470-cff9-11e7-86d0-83752e057225/things/87456840-e0eb-11e9-a38a-d57172a4b4d4/data/2
#       Channel = str(msg.topic)[-2:]
       null,null,null,null,null,Channel = str(msg.topic).split(sep='/')
       null,Data = str(msg.payload).rstrip("'").split(sep='=')
       print("Parsed: ", Channel, Data )


client = cayenne.client.CayenneMQTTClient()

CONNECTING=True

while CONNECTING:
	try:
		print("Connecting:", time.time())
		client.begin(CayenneParam.get('CayUsername'), \
			   CayenneParam.get('CayPassword'), \
			   CayenneParam.get('CayClientID') \
			)
		CONNECTING=False
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883, loglevel=logging.INFO)
	except ValueError:
		print ("Failed")

# COUNTER=[-41.3,174.78,10]
TIMESTAMP = time.time()

# client.subscribe(Subscribe)
client.on_message = on_message
with open(INPUTFILE, 'r') as CsvFile:
#   TIME RSSI LAT LONG
    reader = csv.reader(CsvFile, delimiter=',')
    next(reader) # skip header
    for ROW in reader :
      client.loop()
      print( ROW[0], ROW[1] )
      LATc=ROW[2]
      LONGc=ROW[3]
      COUNTER=[round(float(LATc),5), round(float(LONGc),5), 100]
      print( CHANNELpub, COUNTER, type(COUNTER) )
      client.virtualWrite(CHANNELpub, COUNTER, "gps", "m")
      time.sleep(Interval)

