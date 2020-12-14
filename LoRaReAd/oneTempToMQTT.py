#!/usr/bin/python
# from: https://www.raspberrypi.org/forums/viewtopic.php?t=128776
# might have originated at https://books.google.co.nz/books?id=0skvDAAAQBAJ&pg=PT517&lpg=PT517&dq=read_temp_raw()+read_temp()&source=bl&ots=oMIeeAhhQd&sig=9hdPtnvkZmE5fsurRFmV8acsGAU&hl=en&sa=X&ved=2ahUKEwjtjsj6me3aAhUCjpQKHb8-A2MQ6AEwAXoECAAQNw#v=onepage&q=read_temp_raw()%20read_temp()&f=false

import logging
import threading
import time
import os
import sys
import cayenne.client
import datetime
import toml
import string
# import requests, glob, uuid, traceback # (Unnecssesary things I used to import)
from SensorLib import GetWirelessStats
from SensorLib import GetSerialData
from SensorLib import ReadTemp
from MQTTUtils import Save2Cayenne
from MQTTUtils import Save2CSV
from MQTTUtils import DataError
from MQTTUtils import PiSerial
# from MQTTUtils import ProcessError
from gpiozero  import CPUTemperature
from gpiozero  import DiskUsage
from gpiozero  import LoadAverage

interval = 10 # Seconds between temperature checks
max_time = 9  # minutes to keep trying to get temperatures

max_temp = 30000 # Maximum degrees to accept (Celcius time 1000)

device_locations = '/sys/bus/w1/devices/'

all_temp = {}
max_time_seconds = max_time * 60

def ReadTempThread(Freq,CSVPath,ClientID,client):
  DoRead = True
  while DoRead :
    try:
      Value = ReadTemp()
#    logging.info("Temp Loop: %s", Value)
      Channel = 'ExtTemp'
      Save2CSV (CSVPath, ClientID, Channel, Value)
      Save2Cayenne (client, Channel, Value, 1)
      time.sleep(Freq)
    except :
      Message = "Exception reading Onboard Temperature"
      CSV_Message = Message
      DoRead = ProcessError(CSVPath, ClientID, '', CSV_Message, Message)


def ReadDiskThread(Freq,CSVPath,ClientID,client):
  DoRead = True
  while DoRead :
    try:
      Value = round( DiskUsage().value,2)
#    logging.info("Disk Loop: %s", Value)
      Channel = 'DiskAvg'
      Save2CSV (CSVPath, ClientID, Channel, Value)
      Save2Cayenne (client, Channel, Value, 1)
      time.sleep(Freq)
    except :
      Message = "Exception reading Disk Usage"
      CSV_Message = Message
      DoRead = ProcessError(CSVPath, ClientID, '', CSV_Message, Message)


def ReadLoadThread(Freq,CSVPath,ClientID,client):
  DoRead = True
  while DoRead :
    try:
      Value = LoadAverage().load_average
#    logging.info("Load Loop: %s", Value)
      Channel = 'LoadAvg'
      Save2CSV (CSVPath, ClientID, Channel, Value)
      Save2Cayenne (client, Channel, Value, 1)
      time.sleep(Freq)
#      raise Exception('Test exception at line 79 of Thread2MQTT.py')
    except :
      Message = "Exception reading Load Average"
      CSV_Message = Message
      DoRead = ProcessError(CSVPath, ClientID, '', CSV_Message, Message)

def ReadCPUThread(Freq,CSVPath,ClientID,client):
  DoRead = True
  while DoRead :
    try:
      Value = CPUTemperature().temperature
#    logging.info("CPU  Loop: %s", Value)
      Channel = 'CPUtemp'
      Save2CSV (CSVPath, ClientID, Channel, Value)
      Save2Cayenne (client, Channel, Value, 1)
      time.sleep(Freq)
    except :
       Message = "Exception reading CPU Temperature"
       CSV_Message = Message
       DoRead = ProcessError(CSVPath, ClientID, '', CSV_Message, Message)


def ReadWifiThread(Freq,CSVPath,ClientID,client):
  DoRead = True
  while DoRead :
    try:
      Value = GetWirelessStats()
#     logging.info("Wifi Loop: %s", Value)
      Link = Value['wlan0']['link']
      Channel = 'WifiLnk'
      Save2CSV (CSVPath, ClientID, Channel, Link)
      Save2Cayenne (client, Channel, Link, 100)
      Level = Value['wlan0']['level']
      Channel = 'WifiLvl'
      Save2CSV (CSVPath, ClientID, Channel, Level)
      Save2Cayenne (client, Channel, Level, 100)
      time.sleep(Freq)
    except :
       Message = "Exception reading Wifi Data"
       CSV_Message = Message
       DoRead = ProcessError(CSVPath, ClientID, '', CSV_Message, Message)

def ProcessError(CSVPath, ClientID, CayClient, CSV_Message, Message):
# Save Message to a file and Cayenne
    global LastError
    CurrentTime = datetime.datetime.now().isoformat()
    CSVPathFile = Save2CSV (CSVPath, ClientID, 'Exception', CSV_Message)
    CurrentTime = datetime.datetime.now().isoformat()
    LogPathFile = logging.getLoggerClass().root.handlers[0].baseFilename

    ErrorTime = datetime.datetime.now()
    ErrorGap    = ErrorTime - LastError['time']
#    logging.info( LastError )
#    logging.info( ErrorGap )

    if ErrorGap.days > 0: # Ages since last error
        Continue = True
        ResetCount = True
    elif ErrorGap.seconds > LastError['period']: # OK time since last error
        Continue = True
        ResetCount = True
    elif LastError['count'] < LastError['threshold']: # Still counting
        LastError['count'] += 1
        Continue = True
        ResetCount = False
    else:      # We have a problem
        Continue = False
        ResetCount = True

    if ResetCount:
        LastError = {
            'time'  : ErrorTime,
            'count' : 0
        }

    if not(Continue):
        Message = Message+' terminating thread'

    logging.exception(Message)
    os.system('tail -20 '+LogPathFile) # display last error if in foreground
    if CayClient :
        Save2Cayenne (CayClient, 'Stat', -1, 1)

    return(Continue)



def read_temp ():

	target_folders = [ '28-0417019fa4ff', '28-041671ea1aff', '28-041701ae78ff', '28-041701bcc3ff' ]
	target_results = {}

	# Set up the location of the DS18B20 sensors in the system
	device_folders = glob.glob(os.path.join(device_locations,'28*'))

	print ( datetime.datetime.now().isoformat(), len(device_folders) ) # Number of folders found

	device_files = []
	while device_folders :
		device_files.append(os.path.join(device_folders.pop(-1),'temperature'))

#	while target_folders :

	while device_files :
		this_file = device_files.pop(-1)
		bit = this_file.split('/')
		this_device = bit[5]
		this_content = open(this_file, 'r')
		this_temp = this_content.readlines()
		this_content.close()
		if len( this_temp ) > 0 :
			if int (this_temp[0]) < max_temp :
			# Don't want to try getting element of empty list or making empty string into int
				target_results[this_device] = int (this_temp[0])

#		print ( this_file, this_device, this_temp )
#		print (target_results, max_temp)
	return target_results


# if not any( V is None for V in LOCATION.values()):

repeatChecks = True
start_time = time.time()

HomeDir =       os.environ['HOME']
AUTH_FILE = 	'cayenneMQTT.txt'
LOG_FILE =	'LOG_' + os.path.basename(__file__)
CSV 	= 	'.csv'
CsvTopic = 	'RSSILatLong'
CSVPath =	os.path.join(HomeDir, 'CSVdata')
Eq	= 	' = '
CrLf	= 	'\r\n'
Qt	= 	'"'

# Set up logging and local copies of data
ConfPathFile = os.path.join(HomeDir, AUTH_FILE)
LogPathFile  = os.path.join(CSVPath, LOG_FILE)

format = "%(asctime)s: %(message)s"
logging.basicConfig(filename=LogPathFile, format=format, level=logging.DEBUG,
                        datefmt="%Y-%m-%d_%H:%M:%S")
# logging.basicConfig(filename=LogPathFile, level=logging.DEBUG)
CurrentTime = datetime.datetime.now().isoformat()
ErrorTime = datetime.datetime.now()
logging.debug(CrLf+'***** Starting at: {a}'.format(a=CurrentTime)+' *****' )

# Set up timer for catching repeated errors
LastError = {
    'time'  : ErrorTime,
    'count' : 0,
    'period' : 300, # Time to keep counting 300 seconds = 5 minutes
    'threshold' : 3 # Look for 3 errors in 5 minutes
}

# Cayenne authentication info. This should be obtained from the Cayenne Dashboard,
#  and the details should be put into the file listed above.
# Read the Cayenne configuration stuff into a dictionary
ConfigDict = toml.load(ConfPathFile)
CayenneParam = ConfigDict.get('cayenne')
print (CayenneParam)

# Connect to Cayenne Cloud
client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.on_connect = on_connect

client.begin(CayenneParam.get('CayUsername'), \
    CayenneParam.get('CayPassword'), \
    CayenneParam.get('CayClientID'), \
    )
ClientID = CayenneParam.get('CayClientID')


while repeatChecks:

	all_temp.update( read_temp () )

# 	print(msg_body, target_temp, target_freq )

	if len (all_temp) == 4 or time.time() > (start_time + max_time_seconds) :
		repeatChecks = False
	else :
		timedata = time.time()
		while (time.time() < timedata + interval):
			time.sleep(1)

print( all_temp  )

