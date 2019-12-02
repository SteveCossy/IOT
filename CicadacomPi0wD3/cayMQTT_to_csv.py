# From:Sherman Perry <sherman@shermnz.net>
# Based on: https://www.eclipse.org/paho/clients/python/
# Access from: https://cayenne.mydevices.com/shared/5db546374ed44e3f571c50e9

import os, csv, toml, datetime
import paho.mqtt.client as mqtt
# from datetime import datetime

HomeDir =    os.environ['HOME']
# HomeDir =      '/home/pi'
ConfFile =     '/CicadacomPi0wD3.txt'
CsvPath =      HomeDir+'/'
CSV =           '.csv'
CrLf =          '\r\n'
GeoFile =     'CicadacomPi0wD3'

ConfPathFile = HomeDir+ConfFile

# How often shall we write values to Cayenne? (Seconds + 1)
Interval =      60

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the details should be put into the file listed above.

# Read the Cayenne configuration stuff into a dictionary
ConfigDict = toml.load(ConfPathFile)
CayenneParam = ConfigDict.get('cayenne')
print (CayenneParam)

# Expected config
# [cayenne]
# CayUsername
# CayPassword
# CayClientID
# UniqueID

Subscribe	="v1/{}/things/{}/data/#".format( \
	CayenneParam.get('CayUsername'), \
	CayenneParam.get('CayClientID') )
# The subscribe string we  will send to Cayenne

# Prepare for creating an RSSI, Latitude, Longitude CSV
ChannelMap = {'3':'BAT','1':'LAT','2':'LONG'}
LocationKeys = ['TIME', 'BAT', 'LAT', 'LONG']
Location = {}
for key in ChannelMap:
    Location[ChannelMap[str(key)]] = None

# print(Subscribe)

# def min2dec (RefMinutes):
#      # Accept a geolocation element (longitude or latitude) in degrees.Minutes (String or float)
#      # Return a string repesenting the same element in degrees with decimals
# details in https://github.com/SteveCossy/IOT/blob/master/CicadacomPi0wD3/min2dec

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Subscribe)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic +" & "+ str(msg.payload))
    if "data" in str(msg.topic):
    # test just in case we get a message that is not data (I wonder what we should do with it?)
# eg msg: v1/6375a470-cff9-11e7-86d0-83752e057225/things/87456840-e0eb-11e9-a38a-d57172a4b4d4/data/2
#       Channel = str(msg.topic)[-2:]
       null,null,null,null,null,Channel = str(msg.topic).split(sep='/')
       null,Data = str(msg.payload).rstrip("'").split(sep='=')
       print("Parsed: ", Channel, Data )
       print( Location )
       Location[ChannelMap[Channel]] = Data
       CurrentTime = datetime.datetime.now().isoformat()
       print( Location )
       if not any( LocationValues is None for LocationValues in Location.values()):
       # All values have valid content
           # Note when we assembled this tuple
           Location['TIME'] =	CurrentTime
#           Location['LAT'] =	min2dec (Location['LAT'])
#           Location['LONG'] = 	min2dec (Location['LONG'])
           # Add the whole number (till Andrew starts sending a proper one)
           # Then we have a complete location!
           # Save it, then wait for the next location to turn up
           print("Complete! ", Location, CrLf )
           CsvOut =CsvPath+GeoFile+CSV
           if not os.path.isfile(CsvOut):
           # There is not currently an output file
               print ("Creating new output file: "+CsvOut)
               with open(CsvOut, 'w') as CsvFile:
                    writer = csv.DictWriter(CsvFile, fieldnames=LocationKeys)
                    writer.writeheader()
           with open(CsvOut, 'a') as CsvFile:
               writer = csv.DictWriter(CsvFile, fieldnames=LocationKeys)
               writer.writerow(Location)
           # Reset Location
#           Location = {'TIME': '1'}
           for key in ChannelMap:
              Location[ChannelMap[str(key)]] = None
    
#   if msg.topic.endswith("10") or msg.topic.endswith("11") or msg.topic.endswith("22"):
#   print("{0} {1}".format(msg.topic, str(msg.payload)))
#      print(msg.topic +"&"+ str(msg.payload))

client = mqtt.Client(client_id=CayenneParam.get('UniqueID') )
client.username_pw_set(CayenneParam.get('CayUsername'), \
	CayenneParam.get('CayPassword') )
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.mydevices.com", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

