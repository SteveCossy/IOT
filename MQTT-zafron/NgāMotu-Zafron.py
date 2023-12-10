#!/usr/bin/env python
# Ngā Motu to Zafron
# Steve Cosgrove, started 10 Dec 2023
# Subscribe to data from Nga Motu and publish it to Zafron for Visulalisation
# Currently doing nothing else!

import random, datetime, time, logging, csv, os
import requests, datetime, time, glob, uuid, sys, toml

import paho.mqtt.client as mqtt

# Useful constants
HomeDir = 	os.environ['HOME']
# HomeDir	= '/home/pi'
ConfPathFile = 'MQTT-Zafron.txt'

print (ConfPathFile)

CsvPath = os.path.join(HomeDir,ConfPathFile)
CSV 	= '.csv'
Eq	= ' = '
CrLf	= '\r\n'
Qt	= '"'
# I wonder if I need this? UniqueClientID  = str(int(random.random() * 10**16))+str(int(random.random() * 10**16))

# Read the config file
ConfigDict = toml.load(ConfPathFile)
# Extract details for each server
ParamNga = ConfigDict.get('NgaMotu')
ParamZaf = ConfigDict.get('Zafron')

# What channels do we want?
Subscribe = "penguin/cicada/#"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Subscribe)

def on_message(client, userdata, msg):
    print( 
        msg.topic +" & "+ str(msg.payload), CrLf
        )

NgaClient = mqtt.Client(ParamNga.get('ClientID') )
NgaClient.username_pw_set(ParamNga.get('Username'), \
        ParamNga.get('Password') )

client.on_message = on_message
client.on_connect = on_connect
client.connect(ParamNga.get('Server'), ParamNga.get('Port'), 20)

client.loop_forever()
