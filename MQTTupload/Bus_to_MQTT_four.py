# Read data from two temperature sensors, and send it to designated mosquitto broker
# based on code provided by Steve Cope at www.steves-internet-guide.com
# including http://www.steves-internet-guide.com/client-objects-python-mqtt/

# more documentation: https://pypi.org/project/paho-mqtt/#constructor-reinitialise

# excellent description of how to read multiple sensors
# https://www.raspberrypi.org/forums/viewtopic.php?t=128776

import time, glob, paho.mqtt.client as mqtt, ssl

broker_file = '/home/pi/MQTT_broker'
interval = 5

# Read each line of broker_file, and remove the <CR><LF> at the end of the line
broker_deets = open(broker_file,'r')
line = broker_deets.readline()		# Read the comment line
line = broker_deets.readline()		# IP Address or hostname of MQTT broker
broker_address	=line.rstrip("\r\n")
line = broker_deets.readline()		# Topic Name to use for Value One
broker_topic1	=line.rstrip("\r\n")
line = broker_deets.readline()		# Topic Name to use for Value Two
broker_topic2	=line.rstrip("\r\n")
line = broker_deets.readline()		# Broker username
broker_username	=line.rstrip("\r\n")
line = broker_deets.readline()		# Broker password VERY INSECURE!
broker_password	=line.rstrip("\r\n")
broker_deets.close()

# print( broker_address, broker_topic1, broker_topic2, broker_username, broker_password)

def read_temp_raw(): #A function that grabs the raw temp data from the sensors
	f_1 = open(device_file[0], 'r')
	lines_1 = f_1.readlines()
	f_1.close()
	f_2 = open(device_file[1], 'r')
	lines_2 = f_2.readlines()
	f_2.close()
	f_3 = open(device_file[1], 'r')
	lines_3 = f_3.readlines()
	f_3.close()
	f_4 = open(device_file[1], 'r')
	lines_4 = f_4.readlines()
	f_4.close()
	return lines_1 + lines_2 + lines_3 + lines_4

def read_temp(): #A function to check the connection was good and strip out the temperature
	lines = read_temp_raw()
#	print( lines )
	while lines[0].strip()[-3:] != 'YES' or lines[2].strip()[-3:] != 'YES' or lines[3].strip()[-3:] != 'YES' or lines[4].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
		print( lines )
	equals_pos = lines[1].find('t='), lines[3].find('t=')
	temp = float(lines[1][equals_pos[0]+2:])/1000, float(lines[3][equals_pos[1]+2:])/1000
	return temp

def on_message(client, userdata, message):
	print("message received " ,str(message.payload.decode("utf-8")))
	print("message topic=",message.topic)
	print("message qos=",message.qos)
	print("message retain flag=",message.retain)


# Program starts here

# Connect to the broker
# broker = mqtt.Client()
# broker.username_pw_set(broker_username, broker_password)

# broker.tls_set(
# ca_certs="/home/pi/root.crt" , tls_version=ssl.PROTOCOL_TLSv1
# )
# broker.tls_insecure_set(True)

# Port number should be in a config file, not hard-coded
# broker.connect(broker_address,8883)
# http://www.steves-internet-guide.com/mosquitto-tls/

# broker.on_message=on_message        #attach function to callback
# broker.loop_start()    #start the loop

# This file was: /usr/share/cacti/site/scripts/flow_temps.py
# Set up the location of the DS18B20 sensors in the system
device_folder = glob.glob('/sys/bus/w1/devices/28*')
device_file = [device_folder[0] + '/w1_slave',device_folder[1] + '/w1_slave']

Run_flag=True # Get the loop started

while Run_flag:
	try:  # catch a <CTRL C>

		temps = read_temp() #get the temp
#		print('T1:'+str(temps[0])+' T2:'+str(temps[1]))
#		broker_data1 = temps[0]
#		broker_data2 = temps[1]

#		broker.publish(broker_topic1,broker_data1)
#		broker.publish(broker_topic2,broker_data2)

#		print(broker_topic1, str(broker_data1),broker_topic2, str(broker_data2))
		timedata = time.time()
		while (time.time() < timedata + interval):
			time.sleep(1)
	except KeyboardInterrupt:
		Run_flag=False # Stop the loop

print('\n','Exiting app')	# Send a cheery message
# time.sleep(4) 		# Four seconds to allow sending to finish
# broker.disconnect()	# Disconnect from broker
# broker.loop_stop()	# Stop looking for messages


