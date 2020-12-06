#!/usr/bin/python
# from: https://www.raspberrypi.org/forums/viewtopic.php?t=128776
# might have originated at https://books.google.co.nz/books?id=0skvDAAAQBAJ&pg=PT517&lpg=PT517&dq=read_temp_raw()+read_temp()&source=bl&ots=oMIeeAhhQd&sig=9hdPtnvkZmE5fsurRFmV8acsGAU&hl=en&sa=X&ved=2ahUKEwjtjsj6me3aAhUCjpQKHb8-A2MQ6AEwAXoECAAQNw#v=onepage&q=read_temp_raw()%20read_temp()&f=false

import os, glob, time, sys, datetime

interval = 4 # Seconds between temperature checks

def read_temp ():

	#Set up the location of the DS18B20 sensors in the system
	device_folders = glob.glob('/sys/bus/w1/devices/28*')

	print ( len(device_folders) ) # Number of folders found

	device_files = []
	while device_folders :
		device_files.append(os.path.join(device_folders.pop(-1),'temperature'))

	while device_files :
		this_file = device_files.pop(-)
		this_content = open(this_file, 'r')
		this_temp = this_content.readlines()
		this_content.close()

		print ( this_file, this_temp )


repeatChecks = True

while repeatChecks:

	read_temp ()

# 	print(msg_body, target_temp, target_freq )
	timedata = time.time()
	while (time.time() < timedata + interval):
		time.sleep(1)
#	repeatChecks = False

