###  Record all transactions on local Mosquitto server to csv file
### based on send-receive-file.py by Steve Cope at www.steves-internet-guide.com
import time
import paho.mqtt.client as paho
#import hashlib

broker="localhost"

filepath="/home/mosquitto/"
file_out="mosquitto-all.csv"
topic="#"
crlf='\r\n'

#define callback
def on_message(client, userdata, message):
   # time.sleep(1)
   # print("received message =",str(message.payload.decode("utf-8")))
   fout=open(filepath+file_out,"a")
   fout.write(str(message.payload.decode("utf-8"))+crlf)
   fout.close()
#   print("finished writing message")

client= paho.Client("client-read")
######
client.on_message=on_message

client.mid_value=None
#####
# print("connecting to broker ",broker)
client.connect(broker) #connect
client.loop_start() #start loop to process received messages
# print("subscribing ")
client.subscribe(topic)#subscribe
time.sleep(2)
start=time.time()

Run_flag=True
count=0

while Run_flag:
	try:
		time.sleep(1)
	except:
		Run_flag=False

time_taken=time.time()-start
# print("Ran for ",time_taken)
time.sleep(4)
client.disconnect() #disconnect
client.loop_stop() #stop loop
