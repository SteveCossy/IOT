#!/usr/bin/env python
# Read bits direct from LoRa module and display them, and write too, Steve Cosgrove, 20 Jan 2020

import datetime, time, serial, csv, os, toml, struct, codecs

# python3 -m pip install --user pyserial

# Useful constants
HOME_DIR = 	os.environ['HOME']
# HOME_DIR =	'/home/pi'
AUTH_FILE = 	'cayenneMQTT.txt'
CSV 	= 	'.csv'
CsvTopic = 	'RSSILatLong'
CSVPath =	HOME_DIR # Maybe change later
Eq	= 	' = '
CrLf	= 	'\r\n'
Qt	= 	'"'

# Set up the serial port.

# Default location of serial port on pre 3 Pi models
# SERIAL_PORT =  "/dev/ttyAMA0"

# Default location of serial port on Pi models 3 and Zero
# SERIAL_PORT =   "/dev/ttyS0"

# Bottom right USB port on Pi model 3 
SERIAL_PORT =   "/dev/ttyUSB0"

BAUDRATE=2400
# These values appear to be the defaults
#    parity = serial.PARITY_NONE,
#    stopbits = serial.STOPBITS_ONE,
#    bytesize = serial.EIGHTBITS,

HEADER = b'\xFF\xFF'
ATmode = b'\x1B\x1D'

while True:
  with serial.Serial(SERIAL_PORT, BAUDRATE) as ser:
#      print( 'Sending', HEADER+ATmode )
#      ser.write(HEADER+ATmode)
      PacketIn = ser.read(4)
#      print( codecs.encode(PacketIn, 'hex'), PacketIn )
      print( PacketIn )


