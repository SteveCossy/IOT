###  Record all transactions on local Mosquitto server to csv file
### based on send-receive-file.py by Steve Cope at www.steves-internet-guide.com
import time
import paho.mqtt.client as paho
import hashlib
broker="localhost"

filepath="/home/mosquitto/"
file_out="mosquitto-all.csv"
topic="#"

def process_message(msg):
   """ This is the main receiver code
   """
   if len(msg)==200: #is header or end
      msg_in=msg.decode("utf-8")
      msg_in=msg_in.split(",,")
      if msg_in[0]=="end": #is it really last packet?
         in_hash_final=in_hash_md5.hexdigest()
         if in_hash_final==msg_in[2]:
            print("File copied OK -valid hash  ",in_hash_final)
         else:
            print("Bad file receive   ",in_hash_final)
         return False
      else:
         if msg_in[0]!="header":
            in_hash_md5.update(msg)
            return True
         else:
            return False
   else:
      in_hash_md5.update(msg)
      return True
#define callback
def on_message(client, userdata, message):
   # time.sleep(1)
   # print("received message =",str(message.payload.decode("utf-8")))
   fout=open(filepath+file_out,"ab")
   fout.write(message.payload)
   fout.close()


def on_publish(client, userdata, mid):
    #logging.debug("pub ack "+ str(mid))
    client.mid_value=mid
    client.puback_flag=True  

def c_publish(client,topic,out_message,qos):
   res,mid=client.publish(topic,out_message,qos)#publish
   if res==0: #published ok
      if wait_for(client,"PUBACK",running_loop=True):
         if mid==client.mid_value:
            print("match mid ",str(mid))
            client.puback_flag=False #reset flag
         else:
            raise SystemExit("not got correct puback mid so quitting")
         
      else:
         raise SystemExit("not got puback so quitting")
client= paho.Client("client-read")  #create client object client1.on_publish = on_publish                          #assign function to callback client1.connect(broker,port)                                 #establish connection client1.publish("data/files","on")  
######
client.on_message=on_message
# client.on_publish=on_publish
# client.puback_flag=False #use flag in publish ack
client.mid_value=None
#####
print("connecting to broker ",broker)
client.connect(broker) #connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe(topic)#subscribe
time.sleep(2)
start=time.time()
# print("publishing ")
# send_header(filename)
Run_flag=True
count=0
# out_hash_md5 = hashlib.md5()
# in_hash_md5 = hashlib.md5()

while Run_flag:
	time.sleep(1)

time_taken=time.time()-start
print("took ",time_taken)
time.sleep(4)
client.disconnect() #disconnect
client.loop_stop() #stop loop
fout.close()
