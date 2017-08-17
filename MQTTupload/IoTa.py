#!/usr/bin/env python
import cayenne.client
import time
import random

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "eb68ba50-7c95-11e7-9727-55550d1a07e7"
MQTT_PASSWORD  = "21d595fba02f40c0939153605c75ab85f1f71b01"
MQTT_CLIENT_ID = "3677e5b0-7fa8-11e7-a5d9-9de9b49680ec"

# The callback for when a message is received from Cayenne.
def on_message(message):
  print("reply back, message received: " + str(message))
  # If there is an error processing the message return an error string, otherwise return nothing.

client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

i=0
timestamp = 0

while True:
  client.loop()

  if (time.time() > timestamp + 30):
    a = random.uniform(1.234,9.876)
    client.celsiusWrite(1, a)
    time.sleep(3)

    b = random.randrange(33,77)    
    client.luxWrite(2, b)
    time.sleep(3)

    c = random.randrange(0,100,5)
    client.hectoPascalWrite(3, c)
    time.sleep(3)

    k = random.randint(7,93)
    client.luxWrite(4, k)
	
    timestamp = time.time()
    
    print(timestamp)


