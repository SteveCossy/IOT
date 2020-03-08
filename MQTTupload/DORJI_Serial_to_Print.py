#DORJI_Serial_to_MarkerAPI

#!/usr/bin/env python
#WARNING: This is a TTL serial port and must not have more than 3.3 volts applied to the pins

#this imports the libraries needed
import serial, time
#import needed modules
# import urllib
# import urllib2

#This sets up the serial port ttyAMA0 GPIO. baud rate is the bits per second. 
port = serial.Serial("/dev/ttyAMA0", baudrate=2400)

while True:
       	#read buffer until cr/lf
       	rcv = port.readline()
       	rcv = rcv.rstrip("\r\n")
        print(rcv)
       	attributes = rcv.split(",")
        print(attributes)      	
	#for attribute in attributes:
              #print(attribute)
       	param, key = attributes[0].split("=",1)
       	param, node = attributes[1].split("=",1)
       	param, channel = attributes[2].split("=",1)
       	param, data = attributes[3].split("=",1)
       	print(key, node, channel, data)

