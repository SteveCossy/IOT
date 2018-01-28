#!/usr/bin/env python3
import time, serial, paho.mqtt.client as paho

#print( 'Opening MQTT3:',time.ctime(time.time()) )

# mosquitto settings
#broker="home.rata.co.nz"
broker="192.168.80.222"
#broker="sensor-base"
port=8884
qos=1
topic="sensor/temp"

# How often shall we write values to the Mosquitto broker? (Seconds + 1)
interval = 	10

# Default location of serial port on Pi models 1 and 2
SERIAL_PORT =	"/dev/ttyAMA0"

# Set some variables now, in case the error capture below wants to
#  print them before the loop is first run
channel	= -1
node 	= -1
data 	= -1

#This sets up the serial port specified above. baud rate is the bits per second.
sport = serial.Serial(SERIAL_PORT, baudrate=2400, timeout=1)

def on_publish(client, userdata, mid):
#    print("pub ack "+ str(mid))
    client.mid_value=mid
    client.puback_flag=True

# Wait for publish to be acknowledged
def wait_for(client,msgType,period=0.25,wait_time=40):
#def wait_for(client,msgType,period=0.25,wait_time=40,running_loop=False):
#    client.running_loop=running_loop #if using external loop
    wcount=0
    while True:
        #print("waiting"+ msgType)
        if msgType=="PUBACK":
            if client.on_publish:
                if client.puback_flag:
                    return True

        time.sleep(period)
        #print("loop flag ",client.running_loop)
        wcount+=1
        if wcount>wait_time:
            print("return from wait loop taken too long")
            return False
    return True

def c_publish(client,topic,out_message,qos):
   res,mid=client.publish(topic,out_message,qos)#publish
   if res==0: #publish attempted ok
#      if wait_for(client,"PUBACK"):
#      if wait_for(client,"PUBACK",running_loop=True):
         time.sleep(4) # wait for the publish to be acknowledged
         if mid==client.mid_value:
#            print("match mid ",str(mid))
            client.puback_flag=False #reset flag
         else:
            raise SystemExit("not got correct puback mid so quitting")
 #     else:
 #        raise SystemExit("not got puback so quitting")


#####
# Everything defined - so now we can do things
#####

client= paho.Client(topic.replace('/','-'))
client.tls_set('/home/mosquitto/certs/m2mqtt_srv.crt')
client.tls_insecure_set(True)

client.on_publish=on_publish
client.puback_flag=False #use flag in publish ack
client.mid_value=None

#print("connecting to broker ",broker)
client.connect(broker,port)#connect
client.loop_start() #start loop to process received messages

#print( 'Connected:',time.ctime(time.time()) )

# Initialise timing variables 
timedata = time.time()
Run_flag=True

while Run_flag:
	try:  # add an exception capture once everything is working
		rcv = sport.readline() #read buffer until cr/lf
		rcv=rcv.decode("utf-8") #buffer read is 'bytes' in Python 3.x
					#this makes it 'str'
		rcv = rcv.rstrip("\r\n")
#		print("Read: >" + rcv + "<", rcv.count(','))
		if rcv.count(',') > 1:	# Checksum check should be added here
			out_message=str(int(time.time()))+":"+topic+rcv
			c_publish(client,topic,out_message,qos)
#			print( 'Waiting:',time.ctime(time.time()) )
			while (time.time() < timedata + interval):
				time.sleep(1)
			timedata = time.time()
	except KeyboardInterrupt:
		Run_flag=False

time.sleep(4)
client.disconnect() #disconnect
client.loop_stop() #stop loop

