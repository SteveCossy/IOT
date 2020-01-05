#!/usr/bin/env python
# Major update, Steve Cosgrove, 25 Nov 2019

import random, datetime, time, logging, csv, os, requests, datetime, time, glob, uuid, sys, toml
import paho.mqtt.client as mqtt

# python3 -m pip install --user pyserial

# Useful constants
HomeDir = 	os.environ['HOME']
# HomeDir	= '/home/pi'
ConfFile = '/CicadacomPi3~f9ac.txt'

CsvPath = HomeDir+'/'
CSV 	= '.csv'
CrLf 	= '\r\n'
CsvTopic = 'RSSILatLong'
Eq	= ' = '
CrLf	= '\r\n'
Qt	= '"'

CHANNELpub = 22
CHANNELsub = 12
ConfPathFile = HomeDir+ConfFile
# INPUTFILE = "RSSILatLong-TrainingDec2019.csv"

COUNTER=[-41.29838,174.74505,100]

# How often shall we write values to Cayenne? (Seconds + 1)
Interval =      1

# Read the Cayenne configuration stuff into a dictionary
ConfigDict = toml.load(ConfPathFile)
CayenneParam = ConfigDict.get('cayenne')
print (CayenneParam)

UniqueClientID  = str(int(random.random() * 10**16))+str(int(random.random() * 10**16))
# Expected config
# [cayenne]
# CayUsername
# CayPassword
# CayClientID
# UniqueID

Subscribe       ="v1/{}/things/{}/#".format( \
        CayenneParam.get('CayUsername'), \
        CayenneParam.get('CayClientID')
	)
# The subscribe string we  will send to Cayenne

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Subscribe)

def on_message(client, userdata, msg):
    print( \
#        client.name, CrLf, \
#        userdata, CrLf, \
        msg.topic +" & "+ str(msg.payload), CrLf \
        )
#    if "data" in str(msg.topic):
    # test just in case we get a message that is not data (I wonder what we should do with it?)
# eg msg: v1/6375a470-cff9-11e7-86d0-83752e057225/things/87456840-e0eb-11e9-a38a-d57172a4b4d4/data/2
#       Channel = str(msg.topic)[-2:]
#       null,null,null,null,null,Channel = str(msg.topic).split(sep='/')
#       null,Data = str(msg.payload).rstrip("'").split(sep='=')
#       print("Parsed: ", Channel, Data )

client = mqtt.Client(UniqueClientID )
client.username_pw_set(CayenneParam.get('CayUsername'), \
        CayenneParam.get('CayPassword') )
# client.on_connect = on_connect
client.on_message = on_message
client.on_connect = on_connect
client.connect("mqtt.mydevices.com", 1883, 60)

# client.subscribe(Subscribe)

client.loop_forever()





