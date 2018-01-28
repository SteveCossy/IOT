#!/usr/bin/env python3
import cayenne.client, time, paho.mqtt.client as paho

print( 'Opening MQTT3:',time.ctime(time.time()) )

cayenne_authFile = '/home/mosquitto/cayanneMQTT.txt'

# How often shall we write values to Cayenne? (Seconds + 1)
interval = 	60

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the details should be put into the file listed here.

fileContent = open(cayenne_authFile,'r')
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


# Constants to read local broker
#broker_src="localhost"
broker_src="sensor-base"
port=8884
qos=1
topic="#"
crlf='\r\n'

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

# The callback for when a message is received from Cayenne.
def on_message_c(message):
	time.sleep(1)
	print("reply back, message received: " + str(message))
  # If there is an error processing the message return an error string, otherwise return nothing.

def on_message_s(client, userdata, message):
#	time.sleep(1)
#	print("received message =",str(message.payload.decode("utf-8")))
	rcv = str(message.payload.decode("utf-8"))
#	Timestamp:topic:Channel = alpha, data2 = 0-255, checksum,
	timestamp,topic,rcv = rcv.split(':')
#	print("Read: >" + rcv + "<", rcv.count(','))
	node,channel,data,chksum = rcv.split(",")
#	print("rcv: " + node + channel + data )
#                       details = sensor_nodes.get(node)
	if channel == 'A':
		data = int(data)/10
		client_dest.celsiusWrite(1, data)
		client_dest.loop()
#	elif channel == 'B':

print( 'Starting:',time.ctime(time.time()) )

client_src= paho.Client("client-cayanne")
client_src.tls_set('/home/mosquitto/certs/m2mqtt_srv.crt')

client_src.on_message=on_message_s

print("connecting to source broker ",broker_src)
client_src.connect(broker_src,port) #connect
client_src.loop_start() #start loop to process received messages

print("subscribing ")
client_src.subscribe(topic)#subscribe
time.sleep(2)
start=time.time()

print("connecting to Cayenne ",time.ctime(time.time()) )
client_dest = cayenne.client.CayenneMQTTClient()
# client_dest.on_message = on_message_c
client_dest.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

print( 'Connected:',time.ctime(time.time()) )

# Initialise timing variables - each loop will fail first time through
timedata = 0

Run_flag=True
count=0

while Run_flag:
        try:
                time.sleep(1)
        except KeyboardInterrupt:
                Run_flag=False

time.sleep(4)
client_src.disconnect() #disconnect
client_src.loop_stop() #stop loop
