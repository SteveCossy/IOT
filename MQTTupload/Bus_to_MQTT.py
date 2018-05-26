# Read data from two temperature sensors, and send it to designated mosquitto broker
# based on code provided by Steve Cope at www.steves-internet-guide.com
""" Send File Using MQTT """
import time
import paho.mqtt.client as paho

broker_file = '/home/pi/MQTT_broker

broker_deets = open(broker_file,'r')
comment = broker_deets.readline()
broker_server = broker_deets.readline()
broker_server = broker_deets.readline()
broker_server = broker_deets.readline()
broker_server = broker_deets.readline()

broker="home.rata.co.nz"

def on_publish(client, userdata, mid):
    #logging.debug("pub ack "+ str(mid))
    client.mid_value=mid
    client.puback_flag=True  

## waitfor loop
def wait_for(client,msgType,period=0.25,wait_time=40,running_loop=False):
    client.running_loop=running_loop #if using external loop
    wcount=0  
    while True:
        #print("waiting"+ msgType)
        if msgType=="PUBACK":
            if client.on_publish:        
                if client.puback_flag:
                    return True
     
        if not client.running_loop:
            client.loop(.01)  #check for messages manually
        time.sleep(period)
        #print("loop flag ",client.running_loop)
        wcount+=1
        if wcount>wait_time:
            print("return from wait loop taken too long")
            return False
    return True 

client= paho.Client("client-001")  #create client object client1.on_publish = on_publish                          #assign function to callback client1.connect(broker,port)                                 #establish connection client1.publish("data/files","on")  
######
client.on_message=on_message
client.on_publish=on_publish
client.puback_flag=False #use flag in publish ack
client.mid_value=None
#####
print("connecting to broker ",broker)
client.connect(broker)#connect
client.loop_start() #start loop to process received messages
print("subscribing ")
client.subscribe(topic)#subscribe
time.sleep(2)
start=time.time()
print("publishing ")
send_header(filename)
Run_flag=True
count=0
out_hash_md5 = hashlib.md5()
in_hash_md5 = hashlib.md5()

while Run_flag:
   chunk=fo.read(data_block_size)
   if chunk:
      out_hash_md5.update(chunk) #update hash
      out_message=chunk
      #print(" length =",type(out_message))
      c_publish(client,topic,out_message,qos)
         
   else:
      #end of file so send hash
      out_message=out_hash_md5.hexdigest()
      send_end(filename)
      #print("out Message ",out_message)
      res,mid=client.publish("data/files",out_message,qos=1)#publish
      Run_flag=False
time_taken=time.time()-start
print("took ",time_taken)
time.sleep(4)
client.disconnect() #disconnect
client.loop_stop() #stop loop
fout.close()
fo.close()
