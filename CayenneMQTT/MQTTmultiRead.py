# Subscribe to a supplied list of MQTT topics
# Started from https://github.com/SteveCossy/IOT/blob/master/CayenneMQTT/cayMQTT_to_csv.py
# Steve Cosgrove, 23 Jan 2021

import os, csv, toml, datetime, sys
import paho.mqtt.client as mqtt

HomeDir =	os.environ['HOME']

# the IOT/LoRaReAd dir contains MQTTUtils.py
MQTTUpath =	os.path.join(HomeDir,'IOT/LoRaReAd')
sys.path.append(MQTTUpath)
from MQTTUtils import Save2CSV

ConfFile =	'/MQTTmultiRead.txt'
# LocPath = 	os.path.join(HomeDir,'CayMQTT')
CSVPath =	os.path.join(HomeDir,'CSVfiles')
CSV =		'.csv'
CrLf = 		'\r\n'
ConfPathFile =	os.path.join(HomeDir,ConfFile)

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the details should be put into the file listed above.

# Read the Cayenne configuration stuff into a dictionary
ConfigDict = toml.load(ConfPathFile)
MQTTdetails = ConfigDict.get('MQTTdetails')
print (MQTTdetails)

# Expected config
# [cayenne]
# CayUsername
# CayPassword
# CayClientID
# UniqueID

Subscribe	="v1/{}/things/{}/data/#".format( \
	MQTTdetails.get('MQTTUsername'), \
	MQTTdetails.get('MQTTClientID') )
# The subscribe string we  will send to the MQTT broker
# should be in the config file

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
        Save2CSV (CSVPath, MQTTdetails.get('MQTTClientID'), Channel, Data)

client = mqtt.Client(client_id=MQTTdetails.get('UniqueID') )
client.username_pw_set(MQTTdetails.get('MQTTUsername'), \
  	MQTTdetails.get('MQTTPassword') )
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTTdetails.get('MQTThost'), \
    MQTTdetails.get('MQTTport'), \
    MQTTdetails.get('MQTTtimeout'))

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
try:  # catch a <CTRL C>
  client.loop_forever()
except KeyboardInterrupt:
  loop.stop() # Stop the loop
  print ()
