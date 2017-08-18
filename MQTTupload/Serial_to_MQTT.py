#!/usr/bin/env python
import cayenne.client, time, serial
# import random

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.

# Random Thing on Steve's Desktop
# MQTT_USERNAME  = "eb68ba50-7c95-11e7-9727-55550d1a07e7"
# MQTT_PASSWORD  = "21d595fba02f40c0939153605c75ab85f1f71b01"
# MQTT_CLIENT_ID = "3677e5b0-7fa8-11e7-a5d9-9de9b49680ec"

# Steve Temperature on Andrew's desktop
MQTT_USERNAME  = "a6f9ca60-aaa6-11e6-839f-8bfd46afe676"
MQTT_PASSWORD  = "55274c8e564557058e1624859307009755186a34"
MQTT_CLIENT_ID = "53a9e530-83b2-11e7-a9f6-4b991f8cbdfd"

# Other settings that seem to be embedded in Cayenne's libraries
# MQTT_URL =	"mqtt.mydevices.com"
# MQTT_PORT =	"1883"

# Default location of serial port on Pi models 1 and 2
SERIAL_PORT =	"/dev/ttyAMA0"

# How often shall we write values to Cayenne? (Seconds + 1)
interval = 	3

#This sets up the serial port specified above. baud rate is the bits per second.
port = serial.Serial(SERIAL_PORT, baudrate=2400, timeout=1)

# The callback for when a message is received from Cayenne.
def on_message(message):
  print("reply back, message received: " + str(message))
  # If there is an error processing the message return an error string, otherwise return nothing.

client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

i=0
timestamp = 0

while True:
	try:
                rcv = port.readline() #read buffer until cr/lf
#                print("Read: >" + rcv + "<")
                rcv = rcv.rstrip("\r\n")
                if len(rcv) > 5:
			# Channel = alpha, data2 = 0-255, checksum,
			channel,node,data, = rcv.split(",")
                      	print("rcv: " + channel + node + data)
			if node == 'A':
				data = int(data)/10
				client.celsiusWrite(1, data)
				client.loop()

 				while (time.time() < timestamp + interval):
					time.sleep(1)

    		timestamp = time.time()
#    		print(timestamp)
	except ValueError:
                print("opps..."+"rcv: " + channel + node + data)

