# From:Sherman Perry <sherman@shermnz.net>
# Based on: https://www.eclipse.org/paho/clients/python/
# Access from: https://cayenne.mydevices.com/shared/5db546374ed44e3f571c50e9

import os, csv, toml, datetime, sys
import paho.mqtt.client as mqtt
# from datetime import datetime

HomeDir =	os.environ['HOME']

# the IOT/LoRaReAd dir contains MQTTUtils.py
MQTTUpath =	os.path.join(HomeDir,'IOT/LoRaReAd')
sys.path.append(MQTTUpath)
from MQTTUtils import Save2CSV

ConfFile =	'/cayenneMQTT.txt'
LocPath = 	os.path.join(HomeDir,'CayMQTT')
CSVPath =	os.path.join(HomeDir,'CSVfiles')
CSV =		'.csv'
CrLf = 		'\r\n'
GeoFile =	'RSSILatLong'

ConfPathFile =	HomeDir+ConfFile

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the details should be put into the file listed above.

# Read the Cayenne configuration stuff into a dictionary
ConfigDict = toml.load(ConfPathFile)
CayenneParam = ConfigDict.get('cayenne')
# print (CayenneParam)

# Expected config
# [cayenne]
# CayUsername
# CayPassword
# CayClientID
# UniqueID

Subscribe	="v1/{}/things/{}/data/#".format( \
	CayenneParam.get('CayUsername'), \
	CayenneParam.get('CayClientID') )
# The subscribe string we  will send to Cayenne

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Subscribe)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic +"&"+ str(msg.payload))
    if "data" in str(msg.topic):
    # test just in case we get a message that is not data (I wonder what we should do with it?)
# eg msg: v1/6375a470-cff9-11e7-86d0-83752e057225/things/87456840-e0eb-11e9-a38a-d57172a4b4d4/data/2
       null,null,null,null,null,Channel = str(msg.topic).split(sep='/')
       null,Data = str(msg.payload).rstrip("'").split(sep='=')
       print("Parsed: ", Channel, Data )
       Save2CSV (CSVPath, CayenneParam.get('CayClientID'), Channel, Data)

client = mqtt.Client(client_id=CayenneParam.get('UniqueID') )
client.username_pw_set(CayenneParam.get('CayUsername'), \
	CayenneParam.get('CayPassword') )
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.mydevices.com", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

