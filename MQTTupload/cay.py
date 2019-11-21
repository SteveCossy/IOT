# From:Sherman Perry <sherman@shermnz.net>
# Based on: https://www.eclipse.org/paho/clients/python/

import os
import paho.mqtt.client as mqtt

# home_dir =    os.environ['HOME']
home_dir =      '/home/pi'
auth_file =     'cayanneMQTT.txt'
csv_path =      home_dir+'/'
csv =           '.csv'
crlf =          '\r\n'
csv_topic =     'RSSILatLog'

cayenne_authFile = os.path.join(home_dir, auth_file)

# How often shall we write values to Cayenne? (Seconds + 1)
interval =      60

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the details should be put into the file listed above.
comment, MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID = '', '', '', ''
with open(cayenne_authFile,'r') as fc:
    comment, MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID = fc.read().splitlines()[:4]

SUBSCRIBE	="v1/{}/things/f69ea390-f519-11e9-b49d-5f4b6757b1bf/data/#".format(MQTT_USERNAME)
# print(SUBSCRIBE)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(SUBSCRIBE)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic.endswith("10") or msg.topic.endswith("11") or msg.topic.endswith("22"):
        print("{0} {1}".format(msg.topic, str(msg.payload)))

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