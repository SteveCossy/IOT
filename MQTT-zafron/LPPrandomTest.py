#!/usr/bin/python
"""
CayenneLPP test module.

Some inspireation from: https://github.com/jojo-/py-cayenne-lpp/blob/master/cayenneLPP/cayenneLPP.py

That project was written in 2018 by Johan Barthelemy, who included this description:
The Cayenne LPP aims to facilate the conversion of values typically read from sensors to a
sequence of bits (the payload) that can be send over a network using the
Cayenne Low Power Packet format. This format is particularly suited for LPWAN
networks such as LoRaWAN.
The module consists of a Dictionary defining the different sensors and their size
and a some very rough code sending data to Cayenne.
The constants have the format NAME_SENSOR = (LPP id, Data size) where LPP id
is the IPSO id - 3200 and Data size is the number of bytes that must be used
to encode the reading from the sensor.
More info here:
https://mydevices.com/cayenne/docs/lora/#lora-cayenne-low-power-payload-overview

Original source code is governed by the MIT license that can be found in the
LICENSE file.
"""

__version__ = '0.1'
__author__  = 'Steve Cosgrove'

import struct
import logging
import time
import os
import sys
import datetime
import toml
import string
import glob
import paho.mqtt.client as mqtt
import random	# For generating random example data

# A dictionary of lists of the form
# NAME_SENSOR = [LPP id = IPSO id - 3200, Data size in byte, Data Value]

LPPvalues = {}

LPPvalues ["DIGITAL_INPUT"]	 = [0,1,6]	# 1 unsigned (True/False)
LPPvalues ["DIGITAL_OUTPUT"]     = [1,1,0]	# 1 unsigned (True/False)
LPPvalues ["ANALOG_INPUT"]       = [2,2,0]	# 0.01 signed
LPPvalues ["ANALOG_OUTPUT"]      = [3,2,0]	# 0.01 signed
LPPvalues ["ILLUMINANCE_SENSOR"] = [101,2,0]	# 1 lux unsigned MSB
LPPvalues ["PRESENCE_SENSOR"]    = [102,1,0]	# 1 unsigned (True/False)
LPPvalues ["TEMPERATURE_SENSOR"] = [103,2,0]	# 0.1 deg Celcius signed MSB
LPPvalues ["HUMIDITY_SENSOR"]    = [104,1,0]	# 0.5 unsigned
LPPvalues ["ACCELEROMETER"]      = [113,6,0]	# 0.001 G signed MSB per axis
LPPvalues ["BAROMETER"]          = [115,2,0]	# 0.1 hPa unsigned MSB
LPPvalues ["GYROMETER"]          = [134,6,0]	# 0.01 deg/sec signed msb per axis
LPPvalues ["GPS"]                = [136,9,0]	# latitude:  0.0001 degree signed M>
                                      	# longiture: 0.0001 degree signed M>
                                      	# altitude:  0.01 meter signed MSB

ConfFile = 'CayenneLPPdemo.txt'
HomeDir =       os.environ['HOME']
ConfPathFile = 	os.path.join(HomeDir,ConfFile)
CrLf	= '\r\n'
BROKER_ADDR = 'mqtt.mydevices.com'
BROKER_PORT = 1883

# Read the Cayenne configuration stuff into a dictionary
# Created by https://github.com/SteveCossy/IOT/blob/master/CayenneMQTT/MkAuthSettings.py
# Or a text editor
# Filename is given above in 'ConfFile' variable above
# File should be user's home directory eg '/home/pi/'
# Contents should be copied from a Cayenne 'thing' dashboard eg:
# [cayenne]
# CayUsername = "6375a470-cff9-11e7-86d0-83752e057225"
# CayPassword = "26e1dc13f900da7b30b24cad4b320f9bc6dd0d78"
# CayClientID = "f69ea390-f519-11e9-b49d-5f4b6757b1bf"
# UniqueID = "PythonClient0x5056bfc415"  (or whatever you like)

ConfigDict = toml.load(ConfPathFile)
CayenneParam = ConfigDict.get('cayenne')
print (CayenneParam)
MQTT_USERNAME	= CayenneParam.get('CayUsername')
MQTT_PASSWORD	= CayenneParam.get('CayPassword')
MQTT_CLIENT_ID	= CayenneParam.get('CayClientID')

SUBSCRIBE       ="v1/{}/things/{}/#".format( \
        MQTT_USERNAME, \
        MQTT_CLIENT_ID
	)
TOPIC_PREFIX	="v1/{}/things/{}/".format( \
        MQTT_USERNAME, \
        MQTT_CLIENT_ID
	)
MQTT_UNIQUE_ID = MQTT_CLIENT_ID
# MQTT_UNIQUE_ID = str(int(random.random() * 10**16))+str(int(random.random() * 10**16))
# For use with subscribing only.  Must use Cayenne Client ID to publish data.
COUNTER = 1

# The callback for when a message is received from Cayenne.
def on_message(client, userdata, message):
# based on https://developers.mydevices.com/cayenne/docs/cayenne-mqtt-api/#cayenne-mqtt-api-mqtt-messaging-topics-send-actuator-updated-value
#    global COUNTER
    print("message received: " ,str(message.payload.decode("utf-8")))
    print("message topic: ",message.topic)
    print("message qos: ",message.qos)
    print("message retain flag: ",message.retain)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # for this test we are not subscribing to anything
    # client.subscribe(SUBSCRIBE)

client = mqtt.Client(MQTT_UNIQUE_ID)
client.on_message = on_message
client.on_connect = on_connect
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD )
client.connect(BROKER_ADDR)
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, loglevel=logging.INFO )
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883, loglevel=logging.INFO)

# client.subscribe(SUBSCRIBE)
# client.loop_forever()
# client.loop_start()

def PublishCayenneLPP (payLoad):
    # Hacked from https://github.com/SteveCossy/IOT/blob/master/test/MQTT-Button.py
    # payLoad is the LPP data to publish
#    client.publish(TOPIC_PREFIX+'data/'+payLoad)

    print("Pretending to send",CrLf, \
        "Data type: {0}, Data size: {1}, Data value: {2}" \
        .format( payLoad[0],payLoad[1],payLoad[2]) \
         )
    print ( CrLf)

#   Example of for loop itterating over a Dictionary
#    for key in ChannelMap :
#        ChannelMap[key]         = ord(key)-64           # A=1 B=2 etc


LPPvalues ["ILLUMINANCE_SENSOR"] = [101,2,100]    # 1 lux unsigned MSB

PublishCayenneLPP (LPPvalues ["ILLUMINANCE_SENSOR"])



# Early debugging
# print (LPPvalues)
# print (LPPvalues["DIGITAL_INPUT"][2])


