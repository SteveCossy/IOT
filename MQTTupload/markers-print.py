#!/usr/bin/env python WARNING: This is a TTL serial port 3.3 volts!

#SETUP --------------------------------------------
#this imports the libraries needed
import serial, time
# , urllib, urllib2

#This sets up the serial port ttyAMA0 GPIO. baud rate is the bits per second.
port = serial.Serial("/dev/ttyAMA0", baudrate=2400, timeout=1)
#delay start

#READ SERIAL --------------------------------------------
port.flushInput()
while True:
        try:
                rcv = port.readline() #read buffer until cr/lf
#                print("Read: >" + rcv + "<")
		if(rcv):
                        rcv = rcv.rstrip("\r\n")
                        if len(rcv) > 5:
# Channel = alpha, data2 = 0-255, checksum,
                                node,channel,data, = rcv.split(",")
#                                if len(channel) == 1 and len(node) < 3:
                         	print("rcv: " + channel + node + data)
		time.sleep(2)
        except ValueError:
                print("opps..."+"rcv: " + channel + node + data)
        	port.flushInput()

