# From:Sherman Perry <sherman@shermnz.net>
# Based on: https://www.eclipse.org/paho/clients/python/
# Access from: https://cayenne.mydevices.com/shared/5db546374ed44e3f571c50e9

import os, csv
import paho.mqtt.client as mqtt

# HOME_DIR =    os.environ['HOME']
HOME_DIR =      '/home/pi'
AUTH_FILE =     'cayenneMQTT.txt'
CSV_PATH =      HOME_DIR+'/'
CSV =           '.csv'
CRLF =          '\r\n'
CSV_TOPIC =     'RSSILatLong'

cayenne_authFile = os.path.join(HOME_DIR, AUTH_FILE)

# How often shall we write values to Cayenne? (Seconds + 1)
interval =      60

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the details should be put into the file listed above.
comment, MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID = '', '', '', ''
with open(cayenne_authFile,'r') as fc:
    comment, MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID = fc.read().splitlines()[:4]

MQTT_CLIENT_ID = "caypySUBrandom"
CAYENNE_CLIENT_ID = "f69ea390-f519-11e9-b49d-5f4b6757b1bf"

SUBSCRIBE	="v1/{}/things/{}/data/#".format(MQTT_USERNAME,CAYENNE_CLIENT_ID)

# Prepare for creating an RSSI, Latitude, Longitude CSV
CHANNEL_MAP = {'22':'RSSI','10':'LAT','11':'LONG'}
LOCATION_KEYS = ['RSSI', 'LAT', 'LONG']
LOCATION = {}
for key in CHANNEL_MAP:
    LOCATION[CHANNEL_MAP[str(key)]] = None

# print(SUBSCRIBE)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(SUBSCRIBE)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic +"&"+ str(msg.payload))
    if "data" in str(msg.topic):
    # test just in case we get a message that is not data (I wonder what we should do with it?)
       CHANNEL = str(msg.topic)[-2:]
       null,DATA = str(msg.payload).rstrip("'").split(sep='=')
       print("Parsed: ", CHANNEL, DATA )
       LOCATION[CHANNEL_MAP[CHANNEL]] = DATA
       print( LOCATION )
       if not any( V is None for V in LOCATION.values()):
           # Add the whole number (till Andrew starts sending a proper one)
           LOCATION['LAT'] = "-41" +LOCATION['LAT'].lstrip('0')
           LOCATION['LONG'] = "174"+LOCATION['LONG'].lstrip('0')
           # Then we have a complete location!
           # Save it, then wait for the next location to turn up
 #          LOCATION = {'LAT': '0.1', 'RSSI': '2', 'LONG': '0.3'}
           print("Complete! ", LOCATION, CRLF )
           csv_out =CSV_PATH+CSV_TOPIC+CSV
           with open(csv_out, 'a') as csvfile:
               writer = csv.DictWriter(csvfile, fieldnames=LOCATION_KEYS)
 #              for data in LOCATION:
               writer.writerow(LOCATION)
 #          csvfile.close()
           # Reset LOCATION
           for key in CHANNEL_MAP:
              LOCATION[CHANNEL_MAP[str(key)]] = None
    
#   if msg.topic.endswith("10") or msg.topic.endswith("11") or msg.topic.endswith("22"):
#   print("{0} {1}".format(msg.topic, str(msg.payload)))
#      print(msg.topic +"&"+ str(msg.payload))

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
