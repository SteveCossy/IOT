# Read data from one temperature sensor

import time, glob
interval = 5

def read_temp_raw(): #A function that grabs the raw temp data from the sensors
	FilePath = open(device_file[0], 'r')
	LineOfDate = FilePath.readlines()
	FilePath.close()
	return LineOfDate

def read_temp(): # Check the connection was good & strip out temperature
	lines = read_temp_raw()
	print( lines )
	while lines[0].strip()[-3:] != 'YES' :
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	temp = float(lines[1][equals_pos+2:])/1000
	return temp

# Program starts here

# This file was: /usr/share/cacti/site/scripts/flow_temps.py
# Set up the location of the DS18B20 sensors in the system
device_folder = glob.glob('/sys/bus/w1/devices/28*')
print( device_folder )

device_file = [device_folder[0] + '/w1_slave']

Run_flag=True # Get the loop started

while Run_flag:
	try:  # catch a <CTRL C>
		temps = read_temp() #get the temp
		print( str(temps))
		timedata = time.time()
		while (time.time() < timedata + interval):
			time.sleep(1)
	except KeyboardInterrupt:
		Run_flag=False # Stop the loop

print('\n','Exiting app')	# Send a cheery message
time.sleep(4) 		# Four seconds to allow sending to finish


