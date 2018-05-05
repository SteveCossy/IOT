#!/usr/bin/python
# This file wss: /usr/share/cacti/site/scripts/flow_temps.py
# from: https://www.raspberrypi.org/forums/viewtopic.php?t=128776
# might have originated at https://books.google.co.nz/books?id=0skvDAAAQBAJ&pg=PT517&lpg=PT517&dq=read_temp_raw()+read_temp()&source=bl&ots=oMIeeAhhQd&sig=9hdPtnvkZmE5fsurRFmV8acsGAU&hl=en&sa=X&ved=2ahUKEwjtjsj6me3aAhUCjpQKHb8-A2MQ6AEwAXoECAAQNw#v=onepage&q=read_temp_raw()%20read_temp()&f=false

import os, glob, time, sys, datetime

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
	print( lines )
	while lines[0].strip()[-3:] != 'YES' or lines[2].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t='), lines[3].find('t=')
	temp = float(lines[1][equals_pos[0]+2:])/1000, float(lines[3][equals_pos[1]+2:])/1000
	return temp

temp = read_temp() #get the temp
print('T1:'+str(temp[0])+' T2:'+str(temp[1]))
