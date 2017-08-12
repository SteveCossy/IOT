#!/usr/bin/env python
import cayenne.client
import time

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "a6f9ca60-aaa6-11e6-839f-8bfd46afe676"
MQTT_PASSWORD  = "55274c8e564557058e1624859307009755186a34"
MQTT_CLIENT_ID = "377428e0-526a-11e7-aaa7-cf0a7ad22796"

# The callback for when a message is received from Cayenne.
def on_message(message):
  print("message received: " + str(message))
  # If there is an error processing the message return an error string, otherwise return nothing.

client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

i=0
timestamp = 0

while True:
  client.loop()

  if (time.time() > timestamp + 30):
    client.celsiusWrite(1, i+10)
    client.luxWrite(2, i*10+20)
    client.hectoPascalWrite(3, i+900)
    timestamp = time.time()
    i = i+2
