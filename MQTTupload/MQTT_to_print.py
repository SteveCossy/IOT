# Read data from two temperature sensors, and send it to designated mosquitto broker
# based on code provided by Steve Cope at www.steves-internet-guide.com
# including http://www.steves-internet-guide.com/client-objects-python-mqtt/

# more documentation: https://pypi.org/project/paho-mqtt/#constructor-reinitialise

import time, glob, paho.mqtt.client as mqtt

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


def on_message(client, userdata, message):
	print(time.ctime(time.time()))
	print("message received " ,message.payload)
	print("message topic=",message.topic)
	print("message qos=",message.qos)
	print("message retain flag=",message.retain)


# Program starts here

# Connect to the broker
broker = mqtt.Client()
broker.username_pw_set(broker_username, broker_password)
broker.connect(broker_address)

broker.subscribe([(broker_topic1,1),(broker_topic2,1)])

broker.on_message=on_message        #attach function to callback
broker.loop_start()    #start the loop

while True :
	try:  # catch a <CTRL C>
		time.sleep(1)
	except KeyboardInterrupt:
                Run_flag=False # Stop the loop

print('\n','Exiting app')       # Send a cheery message
time.sleep(4)           # Four seconds to allow sending to finish
broker.disconnect()     # Disconnect from broker
broker.loop_stop()      # Stop looking for messages

