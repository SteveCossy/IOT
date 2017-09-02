#!/usr/bin/env python
import cayenne.client, time, serial
# import random

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.

# Random Thing on Steve's Desktop
MQTT_USERNAME  = "eb68ba50-7c95-11e7-9727-55550d1a07e7"
MQTT_PASSWORD  = "21d595fba02f40c0939153605c75ab85f1f71b01"
MQTT_CLIENT_ID = "3677e5b0-7fa8-11e7-a5d9-9de9b49680ec"

# Steve Temperature on Andrew's desktop
# MQTT_USERNAME  = "a6f9ca60-aaa6-11e6-839f-8bfd46afe676"
# MQTT_PASSWORD  = "55274c8e564557058e1624859307009755186a34"
# MQTT_CLIENT_ID = "53a9e530-83b2-11e7-a9f6-4b991f8cbdfd"

# Other settings that seem to be embedded in Cayenne's libraries
# MQTT_URL =	"mqtt.mydevices.com"
# MQTT_PORT =	"1883"

# Default location of serial port on Pi models 1 and 2
SERIAL_PORT =	"/dev/ttyAMA0"

# How often shall we write values to Cayenne? (Seconds + 1)
interval = 	3

# Sort out symbols
# http://www.utf8-chartable.de/unicode-utf8-table.pl?utf8=0x&unicodeinhtml=hex
POWER3 = u'\xb3'
DEG = u'\xb0'  # utf code for degree

# Put our sensor metadata into a dictionary of lists
sensor_short = 0
sensor_fullname = 1
sensor_unit = 2
sensor_unitfull = 3

sensor_nodes = {
	'A' : [ 'Temp', 'Temperature', DEG, 'degrees celcius' ],
        'B' : [ 'Humid', 'Humidity', '%', '%' ],
        'C' : [ 'Rain', 'Rainfall', 'mm', 'millimetres' ],
        'D' : [ 'BaroP', 'Barametric Pressure', 'hPa', 'hectopascal' ],
        'E' : [ 'Capacitance', 'Capacitance', 'F', 'farad' ],
        'F' : [ 'Wght', 'Weight', 'g', 'grammes' ],
        'G' : [ 'Light', 'Light', 'lx', 'lux' ],
        'H' : [ 'Density', 'Density (mass)', 'g/cm'+POWER3, 'grammes per cubic centimetre' ],
        'I' : [ 'NodeI', 'Node I sensor data', 'I', 'Units of node I' ],
        'J' : [ 'NodeJ', 'Node J sensor data', 'J', 'Units of node J' ],
	}

# Set some variables now, in case the error capture below wants to
#  print them before the loop is first run
channel	= -1
node 	= -1
data 	= -1

#This sets up the serial port specified above. baud rate is the bits per second.
port = serial.Serial(SERIAL_PORT, baudrate=2400, timeout=1)

# The callback for when a message is received from Cayenne.
def on_message(message):
  print("reply back, message received: " + str(message))
  # If there is an error processing the message return an error string, otherwise return nothing.

client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

timestamp = 0

while True:
#	try:  # add an exception capture once everything is working
                rcv = port.readline() #read buffer until cr/lf
                rcv = rcv.rstrip("\r\n")
                print("Read: >" + rcv + "<")
		if len(rcv) > 5:	# Checksum check should be added here
# 			Channel = alpha, data2 = 0-255, checksum,
			channel,node,data = rcv.split(",")
#			channel,node,data,chksum = rcv.split(",")
#			print("rcv: " + channel + node + data )
			details = sensor_nodes.get(node)
			if node == 'A':
				data = int(data)/10
				client.celsiusWrite(1, data)
				client.loop()
#			elif node == 'B':
		print 'Current', details[sensor_fullname], 'is', str(data)+details[sensor_unit]

		while (time.time() < timestamp + interval):
					time.sleep(1)

    		timestamp = time.time()
#    		print(timestamp)
#	except ValueError:
#                print("opps..."+"rcv: " + channel + node + data)

