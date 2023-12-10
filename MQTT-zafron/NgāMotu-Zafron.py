#!/usr/bin/env python
# Ngā Motu to Zafron
# Steve Cosgrove, started 10 Dec 2023
# Subscribe to data from Nga Motu and publish it to Zafron for Visulalisation
# Currently doing nothing else!

import random, datetime, time, logging, csv, os, json
import requests, datetime, time, glob, uuid, sys, toml

import paho.mqtt.client as mqtt

# Useful constants
HomeDir = os.environ['HOME']
# HomeDir	= '/home/pi'
ConfFile = 'MQTT-Zafron.txt'


ConfPathFile = os.path.join(HomeDir,ConfFile)
CSV 	= '.csv'
Eq	= ' = '
CrLf	= '\r\n'
Qt	= '"'
# I wonder if I need this? UniqueClientID  = str(int(random.random() * 10**16))+str(int(random.random() * 10**16))

# debug print (ConfPathFile)

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
# Str error    MsgIn = json.load(str(msg.payload))
    print (transform_payload(msg.payload))

def transform_payload(payload):

    # Example Decode the payload and split it into values
    values = payload.decode().split(',')

    # Construct the JSON array
#    json_array = [
#        {"channel": 100, "type": "rssi", "unit": "dbm", "value": int(values[0])},
#        {"channel": 101, "type": "snr", "unit": "db", "value": int(values[1]), "name": "SNR"},
#        {"channel": 6, "type": "co2", "unit": "ppm", "value": int(values[2]), "name": "CO2"},
#        {"channel": 107, "type": "voltage", "unit": "v", "value": int(values[3]), "name": "VDD"}
#    ]

 #   # Convert the Python object to a JSON string

#    return json.dumps(json_array)
    return values

NgaClient = mqtt.Client(ParamNga.get('ClientID') )
NgaClient.username_pw_set(ParamNga.get('Username'), \
        ParamNga.get('Password') )

NgaClient.on_message = on_message
NgaClient.on_connect = on_connect
NgaClient.connect(ParamNga.get('Server'), int(ParamNga.get('Port')), 20)

# Main execution
if __name__ == "__main__":
    NgaClient.loop_start()
    while True:
            time.sleep(60)
#        try:
#        except KeyboardInterrupt:
#            NgaClient.loop_stop()
#            NgaClient.disconnect()


