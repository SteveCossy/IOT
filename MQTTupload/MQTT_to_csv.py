
# Read data from two temperature sensors, and send it to designated mosquitto broker
# based on code provided by Steve Cope at www.steves-internet-guide.com
# including http://www.steves-internet-guide.com/client-objects-python-mqtt/

# more documentation: https://pypi.org/project/paho-mqtt/#constructor-reinitialise

import csv, os, requests
import xml.etree.cElementTree as ET
import datetime
#import pandas as pd
#import plotly.tools
#from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
#init_notebook_mode()
import time, glob, paho.mqtt.client as mqtt

home_dir = 	os.environ['HOME']
broker_file =	home_dir+'/MQTT_broker'
csv_path = 	home_dir+'/'
csv =		'.csv'
crlf =		'\r\n'


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
	print(time.ctime(time.time()),"message received:" ,message.payload, "Topic:" ,message.topic)
	csv_topic = message.topic.replace("/","-")
	csv_out = csv_path+csv_topic+csv
	fb = open(csv_out,"a")	
	fb.write(time.ctime(time.time())+","+str(message.payload.decode("utf-8"))+crlf)
#	fb.write('\n')
	fb.close()
#	print("message qos=",message.qos)
#	print("message retain flag=",message.retain)


# Program starts here

# Connect to the broker
broker = mqtt.Client()
broker.username_pw_set(broker_username, broker_password)
broker.connect(broker_address)

broker.subscribe([(broker_topic1,1),(broker_topic2,1)])

broker.on_message=on_message        #attach function to callback
broker.loop_start()    #start the loop

Run_flag=True
while Run_flag :
	try:  # catch a <CTRL C>
		time.sleep(1)
	except KeyboardInterrupt:
                Run_flag=False # Stop the loop

print('\n','Exiting app')       # Send a cheery message
time.sleep(4)           # Four seconds to allow sending to finish
broker.disconnect()     # Disconnect from broker
broker.loop_stop()      # Stop looking for messages

# ------ convert -----

csv_this = open('csv_file_this.csv','w')

#txtfile = open('/home/administrator/MQTT_broker')
#time.ctime(time.time())
#txt_data =message.payload
#message.topic
#txtfile.write('txt_data.txt\n')
