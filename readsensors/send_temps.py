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

