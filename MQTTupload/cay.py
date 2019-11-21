# From:Sherman Perry <sherman@shermnz.net>

import paho.mqtt.client as mqtt

# home_dir =    os.environ['HOME']
home_dir =      '/home/pi'
auth_file =     '/cayanneMQTT.txt'
csv_path =      home_dir+'/'
csv =           '.csv'
crlf =          '\r\n'
csv_topic =     'RSSILatLog'

cayenne_authFile = home_dir+auth_file

# How often shall we write values to Cayenne? (Seconds + 1)
interval =      60

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the details should be put into the file listed above.

fileContent = open(cayenne_authFile,'r')
comment = fileContent.readline()
MQTT_USERNAME  = fileContent.readline()
MQTT_PASSWORD  = fileContent.readline()
MQTT_CLIENT_ID = fileContent.readline()
fileContent.close()

MQTT_USERNAME  = MQTT_USERNAME.rstrip('\n')
MQTT_PASSWORD  = MQTT_PASSWORD.rstrip('\n')
MQTT_CLIENT_ID = MQTT_CLIENT_ID.rstrip('\n')
SUBSCRIBE	="v1/"+MQTT_USERNAME+"/things/f69ea390-f519-11e9-b49d-5f4b6757b1bf/data/22"
SUBSCRIBE2	="v1/"+MQTT_USERNAME+"/things/f69ea390-f519-11e9-b49d-5f4b6757b1bf/data/10"
SUBSCRIBE3	="v1/"+MQTT_USERNAME+"/things/f69ea390-f519-11e9-b49d-5f4b6757b1bf/data/11"
# print(SUBSCRIBE)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(SUBSCRIBE)
    client.subscribe(SUBSCRIBE2)
    client.subscribe(SUBSCRIBE3)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client(client_id=MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.mydevices.com", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()