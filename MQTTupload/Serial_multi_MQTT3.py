#!/usr/bin/env python3
import cayenne.client, time, serial
# import random

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the details should be put into the file listed here.

print( 'Opening MQTT3:',time.ctime(time.time()) )

authFile = '/home/pi/cayanneMQTT.txt'

fileContent = open(authFile,'r')
comment = fileContent.readline()
MQTT_USERNAME  = fileContent.readline()
MQTT_PASSWORD  = fileContent.readline()
MQTT_CLIENT_ID = fileContent.readline()
fileContent.close()

MQTT_USERNAME  = MQTT_USERNAME.rstrip('\n')
MQTT_PASSWORD  = MQTT_PASSWORD.rstrip('\n')
MQTT_CLIENT_ID = MQTT_CLIENT_ID.rstrip('\n')

print (MQTT_USERNAME,' ',MQTT_PASSWORD,' ',MQTT_CLIENT_ID)

# Other settings that seem to be embedded in Cayenne's libraries
# MQTT_URL =	"mqtt.mydevices.com"
# MQTT_PORT =	"1883"

# Default location of serial port on Pi models 1 and 2
SERIAL_PORT =	"/dev/ttyAMA0"

# How often shall we write values to Cayenne? (Seconds + 1)
interval = 	30

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
# def on_message(message):
#	time.sleep(1)
#	print("reply back, message received: " + str(message))
  # If there is an error processing the message return an error string, otherwise return nothing.

# time.sleep(30) # give the system time to get things started

print( 'Starting:',time.ctime(time.time()) )

client = cayenne.client.CayenneMQTTClient()
# client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

print( 'Connected:',time.ctime(time.time()) )

timestamp = 0

while True:
#	try:  # add an exception capture once everything is working
		rcv = port.readline() #read buffer until cr/lf
		rcv=rcv.decode("utf-8") #buffer read is 'bytes' in Python 3.x
					#this makes it 'str'
		rcv = rcv.rstrip("\r\n")
		print("Read: >" + rcv + "<", rcv.count(','))
		if rcv.count(',') > 1:	# Checksum check should be added here
# 			Channel = alpha, data2 = 0-255, checksum,
			node,channel,data,chksum = rcv.split(",")
#			print("rcv: " + node + channel + data )
			details = sensor_nodes.get(node)
			if channel == 'A':
				data = int(data)/10
				client.celsiusWrite(1, data)
				client.loop()
#			elif channel == 'B':
#		print 'Current', details[sensor_fullname], 'is', str(data)+details[sensor_unit]

				print( 'Waiting:',time.ctime(time.time()) )
				while (time.time() < timestamp + interval):
					time.sleep(1)

		timestamp = time.time()
#    		print(timestamp)
#	except ValueError:
#                print("opps..."+"rcv: " + channel + node + data)

