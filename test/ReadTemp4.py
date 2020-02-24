# Read data from two temperature sensors, 

import time, glob

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
		print('T1:'+str(temps[0]))
		broker_data1 = temps[0]

		print(broker_topic1, str(broker_data1))
		timedata = time.time()
		while (time.time() < timedata + interval):
			time.sleep(1)
	except KeyboardInterrupt:
		Run_flag=False # Stop the loop

print('\n','Exiting app')	# Send a cheery message
time.sleep(4) 		# Four seconds to allow sending to finish
