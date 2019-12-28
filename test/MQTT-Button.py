#!/usr/bin/env python
import paho.mqtt.client as mqtt
import toml, os, random
# import logging, toml, os, random

ConfFile = 'CicadacomPi3~f9ac.txt'
HomeDir =       os.environ['HOME']
ConfPathFile = 	os.path.join(HomeDir,ConfFile)
CrLf	= '\r\n'

BROKER_ADDR = 'mqtt.mydevices.com'
BROKER_PORT = 1883

# Read the Cayenne configuration stuff into a dictionary
ConfigDict = toml.load(ConfPathFile)
CayenneParam = ConfigDict.get('cayenne')
print (CayenneParam)

MQTT_USERNAME	= CayenneParam.get('CayUsername')
MQTT_PASSWORD	= CayenneParam.get('CayPassword')
MQTT_CLIENT_ID	= CayenneParam.get('CayClientID')

SUBSCRIBE       ="v1/{}/things/{}/data/#".format( \
        MQTT_USERNAME, \
        MQTT_CLIENT_ID
	)

MQTT_UNIQUE_ID = str(int(random.random() * 10**16))+str(int(random.random() * 10**16))

COUNTER = 1

# The callback for when a message is received from Cayenne.
def on_message(client, userdata, message):
#    global COUNTER
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print("message received: " + str(message))
    print(CrLf)
#    client.virtualWrite(18, COUNTER, "analog", "null")
#    COUNTER = COUNTER + 10
    # If there is an error processing the message return an error string, otherwise return nothing.

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(SUBSCRIBE)

client = mqtt.Client(MQTT_CLIENT_ID)
client.on_message = on_message
client.on_connect = on_connect
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD )
client.connect(BROKER_ADDR)
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, loglevel=logging.INFO )
# For a secure connection use port 8883 when calling client.begin:
# client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID, port=8883, loglevel=logging.INFO)

# client.subscribe(SUBSCRIBE)
client.loop_forever()
# client.loop_start()


