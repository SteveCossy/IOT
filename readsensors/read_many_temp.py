#!/usr/bin/python
# from: https://www.raspberrypi.org/forums/viewtopic.php?t=128776
# might have originated at https://books.google.co.nz/books?id=0skvDAAAQBAJ&pg=PT517&lpg=PT517&dq=read_temp_raw()+read_temp()&source=bl&ots=oMIeeAhhQd&sig=9hdPtnvkZmE5fsurRFmV8acsGAU&hl=en&sa=X&ved=2ahUKEwjtjsj6me3aAhUCjpQKHb8-A2MQ6AEwAXoECAAQNw#v=onepage&q=read_temp_raw()%20read_temp()&f=false

import os, glob, time, sys, datetime

interval = 10 # Seconds between temperature checks
max_time = 9  # minutes to keep trying to get temperatures

max_temp = 30000 # Maximum degrees to accept (Celcius time 1000)

device_locations = '/sys/bus/w1/devices/'

all_temp = {}
max_time_seconds = max_time * 60

def read_temp ():

	target_folders = [ '28-0417019fa4ff', '28-041671ea1aff', '28-041701ae78ff', '28-041701bcc3ff' ]
	target_results = {}

	# Set up the location of the DS18B20 sensors in the system
	device_folders = glob.glob(os.path.join(device_locations,'28*'))

	print ( datetime.datetime.now().isoformat(), len(device_folders) ) # Number of folders found

	device_files = []
	while device_folders :
		device_files.append(os.path.join(device_folders.pop(-1),'temperature'))

#	while target_folders :
	print (device_files)
	while device_files :
		this_file = device_files.pop(-1)
		bit = this_file.split('/')
		this_device = bit[5]
		this_content = open(this_file, 'r')
		this_temp = this_content.readlines()
		this_content.close()
		target_results[this_device] = int (this_temp[0])

#		print ( this_file, this_device, this_temp )
	return target_results

repeatChecks = True

try:
	while repeatChecks:

		all_temp.update( read_temp () )

		print( all_temp )

except KeyboardInterrupt:
	repeatChecks = False


