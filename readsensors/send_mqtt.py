#!/usr/bin/python
# This file wss: /usr/share/cacti/site/scripts/flow_temps.py
# from: https://www.raspberrypi.org/forums/viewtopic.php?t=128776
# might have originated at https://books.google.co.nz/books?id=0skvDAAAQBAJ&pg=PT517&lpg=PT517&dq=read_temp_raw()+read_temp()&source=bl&ots=oMIeeAhhQd&sig=9hdPtnvkZmE5fsurRFmV8acsGAU&hl=en&sa=X&ved=2ahUKEwjtjsj6me3aAhUCjpQKHb8-A2MQ6AEwAXoECAAQNw#v=onepage&q=read_temp_raw()%20read_temp()&f=false

import os, glob, time, sys, datetime

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
# Read your Account Sid and Auth Token from twilio.com/console

dataFile = '/home/pi/twilio_data'
interval = 20 # Seconds between temperature checks

#Set up the location of the DS18B20 sensors in the system
device_folder = glob.glob('/sys/bus/w1/devices/28*')
device_file = [device_folder[0] + '/w1_slave',device_folder[1] + '/w1_slave']

def read_temp_raw(): #A function that grabs the raw temp data from the sensors
	f_1 = open(device_file[0], 'r')
	lines_1 = f_1.readlines()
	f_1.close()
	f_2 = open(device_file[1], 'r')
	lines_2 = f_2.readlines()
	f_2.close()
	return lines_1 + lines_2

def read_temp(): #A function to check the connection was good and strip out the temperature
	lines = read_temp_raw()
#	print( lines )
	while lines[0].strip()[-3:] != 'YES' or lines[2].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t='), lines[3].find('t=')
	temp = float(lines[1][equals_pos[0]+2:])/1000, float(lines[3][equals_pos[1]+2:])/1000
	return temp

def send_txt(client, msg_body, temp_this, temp_that, msg_from, msg_to ):
	temp_this_str = str(temp_this)
	temp_that_str = str(temp_that)

	this_msg = msg_body.replace("%1",temp_this_str)
	this_msg = this_msg.replace("%2",temp_that_str)

#	print (time.ctime(time.time()) )
#	print( this_msg )
#	Now send a txt with the info ...
	message = client.messages.create(body=this_msg,from_=msg_from,to=msg_to)
#	print(message.sid)

last_pass = 0

while True:
	# File contains: SID Auth_Token TargetTemp TargetFreq Frequency SID startMsg txtBody from_nbr to_nbr
	# txtBody eg: Current Temps - This: %1 That: %2
	fileContent = open(dataFile,'r')
	comment = fileContent.readline()
	account_sid = fileContent.readline()		# Twilio ID and Token
	auth_token = fileContent.readline()
	temp_target_parts = fileContent.readline()	# Target for Alert messages : How often to send Alerts
	temp_frequency_s = fileContent.readline()	# How often to sent regular updates
	this_msg = fileContent.readline()		# Text for the first message
	msg_body = fileContent.readline()		# Message to send, with %1 & %2 representing two values to insert
	msg_from = fileContent.readline()		# From phone number, as required by Twilio
	msg_to = fileContent.readline()			# To phone number, which must be authorised in Twilio
	fileContent.close()

	target_temp_s,target_freq_s = temp_target_parts.split(":")
	client = Client(account_sid, auth_token)

	if last_pass == 0 :
		message = client.messages.create(body=this_msg,from_=msg_from,to=msg_to)

	temp_frequency = float(temp_frequency_s) * 60 # Change from minutes to seconds
	target_freq = float(target_freq_s) * 60 # Change from minutes to seconds
	target_temp = float(target_temp_s)

	temps = read_temp() #get the temp
#	print('T1:'+str(temps[0])+' T2:'+str(temps[1]))
	temp_this = temps[0]
	temp_that = temps[1]

	if max( temp_this, temp_that ) > target_temp :
		if time.time() > last_pass + target_freq :
			msg_body = 'ALERT! ' + msg_body
			send_txt(client, msg_body, temp_this, temp_that, msg_from, msg_to )
			last_pass = time.time()

	elif time.time() > last_pass + temp_frequency :
		send_txt(client, msg_body, temp_this, temp_that, msg_from, msg_to )
		last_pass = time.time()

# 	print(msg_body, target_temp, target_freq )
	timedata = time.time()
	while (time.time() < timedata + interval):
		time.sleep(1)

#!/usr/bin/env python3
import cayenne.client, time, serial
#, gspread
# import random
# from oauth2client.service_account import ServiceAccountCredentials

print( 'Opening MQTT3:',time.ctime(time.time()) )

# Google stuff based on https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# in particular, need to create a client_secret.json, and put the file in google-client_secret location
# to use Python 3.x, run: sudo pip3 install gspread oauth2client
# Function list: http://gspread.readthedocs.io/en/latest/

cayenne_authFile = '/home/pi/cayanneMQTT.txt'
# google_client_secret = '/home/pi/client_secret.json'

# How often shall we write values to Cayenne? (Seconds + 1)
interval = 	60

# How often shall we re-auth to Google? (Seconds + 1)
# GoogleAuthTime = 60*45  # Every 45 minutes
# GoogleAuthTime = 60*60*24  # Once a day
# GoogleAuthTime = 60  #Testing

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

# Default location of serial port on Pi models 1 and 2
SERIAL_PORT =	"/dev/ttyAMA0"

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

# Initialise timing variables - each loop will fail first time through
timedata = 0
timeauth = 0 #Ensure Google Auth will run before first data pass

while True:
#	while (time.time() < (timeauth + GoogleAuthTime)):
	#		print("Now "+str(time.time())+", Last loop: "+str(timeauth)+", Delay: " + str(GoogleAuthTime)+", Diff: "+str((time.time() - (timeauth + GoogleAuthTime))))
	#	try:  # add an exception capture once everything is working
			rcv = port.readline() #read buffer until cr/lf
			rcv=rcv.decode("utf-8") #buffer read is 'bytes' in Python 3.x
						#this makes it 'str'
			rcv = rcv.rstrip("\r\n")
#			node,channel,data,chksum = rcv.split(",")
			print("Read: >" + rcv + "<", rcv.count(','))
#			print("Read: >",rcv,node,channel,data,chksum,"<")
#			if chksum == '0':	# Checksum check should be added here
			if rcv.count(',') > 1:
# 				Channel = alpha, data2 = 0-255, checksum,
				node,channel,data,chksum = rcv.split(",")
#				print("rcv: " + node + channel + data )
				details = sensor_nodes.get(node)
				if channel == 'A':
					data = float(data)/10
					print(data)
					client.celsiusWrite(1, data)
					client.loop()
#				elif channel == 'B':
#			print 'Current', details[sensor_fullname], 'is', str(data)+details[sensor_unit]
#					print( 'Writing to Sheet:',time.ctime(time.time()) )
#					rowOfData = [time.strftime("%Y-%m-%d_%H:%M:%S"),node,channel,data]
#					sheet.append_row(rowOfData)
#					print( 'Waiting:',time.ctime(time.time()) )
#					while (time.time() < timedata + interval):
#						time.sleep(1)
#
#			timedata = time.time()
#    			print(timestamp)
#		except ValueError:
#       	         print("opps..."+"rcv: " + channel + node + data)

#	scope = ['https://spreadsheets.google.com/feeds']
#	creds = ServiceAccountCredentials.from_json_keyfile_name(google_client_secret, scope)
	# Find a workbook by name and open the first sheet
	# Make sure you use the right name here.
	
#	gclient = gspread.authorize(creds) # Reauth to Google
#	sheet = gclient.open("IOTdata").sheet1
	# use creds to create a client to interact with the Google Drive API
	
#	timeauth = time.time() # Note when did the last reauth
#	print( 'Finished reauth:',time.ctime(time.time()) )

