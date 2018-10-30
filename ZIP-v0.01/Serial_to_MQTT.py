#!/usr/bin/env python
import cayenne.client, datetime, time, serial
# import random

#Delay Start
#print "Time now = ", datetime.datetime.now().strftime("%H-%M-%S")
#time.sleep(60)
#print "Starting now = ", datetime.datetime.now().strftime("%H-%M-%S")

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME  = "6375a470-cff9-11e7-86d0-83752e057225"
MQTT_PASSWORD  = "26e1dc13f900da7b30b24cad4b320f9bc6dd0d78"
MQTT_CLIENT_ID = "157d1d10-69dd-11e8-84d1-4d9372e87a68"

# Other settings that seem to be embedded in Cayenne's libraries
# MQTT_URL =    "mqtt.mydevices.com"
# MQTT_PORT =   "1883"

# Default location of serial port on Pi models 1 and 2
#SERIAL_PORT =  "/dev/ttyAMA0"

# Default location of serial port on Pi models 3 and Zero
SERIAL_PORT =   "/dev/ttyS0"

# How often shall we write values to Cayenne? (Seconds + 1)
interval =  5

#This sets up the serial port specified above. baud rate is the bits per second timeout seconds
#port = serial.Serial(SERIAL_PORT, baudrate=2400, timeout=5)

#This sets up the serial port specified above. baud rate.  This WAITS for any cr/lf (new blob of data from picaxe)
port = serial.Serial(SERIAL_PORT, baudrate=2400)

# The callback for when a message is received from Cayenne.
def on_message(message):
  print("def on_message reply back, message received: " + str(message))
  # If there is an error processing the message return an error string, otherwise returns nothing.

client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

#Predefine Data Packet objects for python prior to trying to look for them :)
node = ":01"
channel = "A"
data = 123
cs = 0

while True:
  try:
    rcv = port.readline() #read buffer until cr/lf
    #print("Serial Readline Data = " + rcv)
    rcv = rcv.rstrip("\r\n")
    node,channel,data,cs = rcv.split(",")
    #Test Point print("rcv.split Data = : " + node + channel + data + cs)
    if cs == '0':
    #if cs = Check Sum is good = 0 then do the following

      if channel == 'A':
        data = float(data)/1
        client.virtualWrite(1, data, "analog_sensor", "null")
        client.loop()

      if channel == 'B':
        data = float(data)/1
        client.virtualWrite(2, data, "analog_sensor", "null")
        client.loop()

      if channel == 'C':
        data = float(data)/1
        client.virtualWrite(3, data, "analog_sensor", "null")
        client.loop()

      if channel == 'D':
        data = float(data)/1
        client.virtualWrite(4, data, "analog_sensor", "null")
        client.loop()

      if channel == 'E':
        data = float(data)/1
        client.virtualWrite(5, data, "analog_sensor", "null")
        client.loop()

      if channel == 'F':
        data = float(data)/1
        client.virtualWrite(6, data, "analog_sensor", "null")
        client.loop()

      if channel == 'G':
        data = float(data)/1
        client.virtualWrite(7, data, "analog_sensor", "null")
        client.loop()

      if channel == 'H':
        data = float(data)/1
        client.virtualWrite(8, data, "analog_sensor", "null")
        client.loop()

      if channel == 'I':
        data = float(data)/1
        client.virtualWrite(9, data, "analog_sensor", "null")
        client.loop()

      if channel == 'J':
        data = float(data)/1
        client.virtualWrite(10, data, "analog_sensor", "null")
        client.loop()

      if channel == 'K':
        data = float(data)/1
        client.virtualWrite(11, data, "analog_sensor", "null")
        client.loop()

      if channel == 'L':
        data = float(data)/1
        client.virtualWrite(12, data, "analog_sensor", "null")
        client.loop()

  except ValueError:
    #if Data Packet corrupt or malformed then...
    print("Data Packet corrupt or malformed")

