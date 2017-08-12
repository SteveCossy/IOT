#!/usr/bin/env python WARNING: This is a TTL serial port 3.3 volts!

#SETUP --------------------------------------------
#this imports the libraries needed
import serial, time, urllib, urllib2

#This sets up the serial port ttyAMA0 GPIO. baud rate is the bits per second.
port = serial.Serial("/dev/ttyAMA0", baudrate=2400, timeout=1)
#delay start

#SEND TO SERVER ----------------------------------
def send(channel,node,data):
    url = 'http://markers.mtaspiring.school.nz/api/marker'
    data = {
        'user_id' : '2',
        'node' : node,
        'channel' : channel,
        'latitude' : '',
        'longitude' : '',
        'elevation' : '',
        'data' : data
        }

    data_encoded = urllib.urlencode(data)
    req = urllib2.Request(url, data_encoded)
    response = urllib2.urlopen(req)
    #print response.read()

#READ SERIAL --------------------------------------------
port.flushInput()
while True:
        try:
                rcv = port.readline() #read buffer until cr/lf
                if(rcv):
                        rcv = rcv.rstrip("\r\n")
                        if len(rcv) > 5:
                                channel,node,data = rcv.split(",")
                                if len(channel) == 1 and len(node) < 3:
                                    print("rcv: " + channel + node + data)
                                    send(channel, node, data)
        except ValueError:
                #print("opps...")
                port.flushInput()
                            