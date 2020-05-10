# Based on ideas from: https://realpython.com/intro-to-python-threading/
# Steve Cosgrove 28 March 2020
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

# the IOT/LoRaReAd dir contains MQTTUtils.py
# MQTTUpath =     os.path.join(HomeDir,'IOT/LoRaReAd')
# sys.path.append(MQTTUpath)

# The callback for when a message is received from Cayenne.
def on_message(client, userData, message):
# based on https://developers.mydevices.com/cayenne/docs/cayenne-mqtt-api/#cayenne-mqtt-api-mqtt-messaging-topics-send-actuator-updated-value
#    global COUNTER
    print("message received: " ,str(message.payload.decode("utf-8")))

def on_connect(client, userData, flags, rc):
    print("Connected with result code "+str(rc))

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


def ReadGPIOData(CSVPath,ClientID,client):
  # Read serial data from GPIO pins
  #
  #   Define the PicAxe Divisors
  DivisorDict = dict.fromkeys(string.ascii_uppercase)
  for key in DivisorDict :
      DivisorDict[key] =	1
  DivisorDict['A'] =	10 # Soil Moisture
  DivisorDict['B'] =	10 # Temperature
  DivisorDict['S'] =	10 # Kihi-02 Moisture
  DivisorDict['T'] =	10 # Kihi-02 Temperature
  DoRead = True

  SerialDetails = {
    "DeviceName": "/dev/serial0",
  #  "ModuleType": "DRF127x",
    "ModuleType": "DRF126x",
    "BAUDrate": "2400",
    }
  # Could also include other parameters
  #  parity = serial.PARITY_NONE,
  #  stopbits = serial.STOPBITS_ONE,
  #  bytesize = serial.EIGHTBITS,
  # Default location of serial port on Pi models 3 and Zero
  #    SERIAL_PORT =        "/dev/ttyS0"
  # Other serial ports are  "/dev/ttyAMA0" & "/dev/serial0"
  # ModuleType can be Dorji DRF126x or DRF127x

  while DoRead :
      try :
        Value = GetSerialData(CSVPath,ClientID,SerialDetails)
    #    logging.info("Serial Loop: %s", Value)
        Status = Value["Status"]
        
        if Status == 0 :
            Error = "Invalid_Read"
            Save2CSV (CSVPath, ClientID, 'Error', Error)
        else :
            # Status is OK, so write the data ...
 #           Error = Value["Error"]
            Channel =   Value["Channel"]
            Data =      Value["Data"]
            ClientID =  Value["ClientID"]
            RSSI =      Value["RSSI"]
            Save2CSV (CSVPath, ClientID, Channel, Data)
            Save2Cayenne (client, Channel, Data, DivisorDict[Channel])

            if not any ( { int(RSSI) <= 0, int(RSSI) >= 255 } ) : # Probably have a valid RSSI
                Channel = chr(22+ord('A')-1)
                # RSSI is Cayenne channel 22, PicAxe 22nd letter in alphabet
                Data = RSSI
                Save2CSV (CSVPath, ClientID, Channel, Data)
                Save2Cayenne (client, Channel, Data, 1)

        Save2Cayenne (client, 'Stat', Status, 1)
      except :
          Message = "Exception reading LoRa Data from GPIO"
          CSV_Message = Message
          DoRead = ProcessError(CSVPath, ClientID, '', CSV_Message, Message)


def ReadUSBData(CSVPath,ClientID,client):
  # Read serial data from USB port
  #
  #   Define the PicAxe Divisors
  DivisorDict = dict.fromkeys(string.ascii_uppercase)
  for key in DivisorDict :
      DivisorDict[key] =	1
  DivisorDict['A'] =	10 # Soil Moisture
  DivisorDict['B'] =	10 # Temperature
  DivisorDict['S'] =	10 # Kihi-02 Moisture
  DivisorDict['T'] =	10 # Kihi-02 Temperature

  USBport = 'USB0'

  if (USBport in PiSerial() ):
        DoRead = True
        logging.info("USB port found: "+ USBport )
  else:
        Message = "Error looking for "+USBport
        CSV_Message = Message
        DoRead = ProcessError(CSVPath, ClientID, '', CSV_Message, Message)
        # Will try to read (twice) data anyway

  SerialDetails = {
    "DeviceName": "/dev/tty"+USBport,
    "ModuleType": "DRF126x",
    "BAUDrate": "2400",
    }
  # Could also include other parameters
  #  parity = serial.PARITY_NONE,
  #  stopbits = serial.STOPBITS_ONE,
  #  bytesize = serial.EIGHTBITS,
  # Default location of serial port on Pi models 3 and Zero
  #    SERIAL_PORT =        "/dev/ttyS0"
  # Other serial ports are  "/dev/ttyAMA0" & "/dev/serial0"
  # ModuleType can be Dorji DRF126x or DRF127x

  while DoRead :
      try :
        Value = GetSerialData(CSVPath,ClientID,SerialDetails)
    #    logging.info("Serial Loop: %s", Value)
        Status = Value["Status"]

        if Status == 0 :
            Error = "Invalid_Read"
            Save2CSV (CSVPath, ClientID, 'Error', Error)
        else :
            # Status is OK, so write the data ...
            Error = Value["Error"]
            Channel = Value["Channel"]
            Data = Value["Data"]
            ClientID = Value["ClientID"]
            Save2CSV (CSVPath, ClientID, Channel, Data)
            Save2Cayenne (client, Channel, Data, DivisorDict[Channel])

        Save2Cayenne (client, 'Stat', Status, 1)
      except :
          Message = "Exception reading LoRa Data from "+USBport
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


if __name__ == "__main__":

    HomeDir =       os.environ['HOME']
    AUTH_FILE = 	'cayenneMQTT.txt'
    LOG_FILE =	'LOG_' + os.path.basename(__file__)
    CSV 	= 	'.csv'
    CsvTopic = 	'RSSILatLong'
    CSVPath =	os.path.join(HomeDir, 'CSVdata')
    Eq	= 	' = '
    CrLf	= 	'\r\n'
    Qt	= 	'"'

    # Seconds between reading each value internal to this Computer
    TempDelay =	300
    CPUDelay =	300
    LoadDelay =	600
    DiskDelay =	900
    WifiDelay =	300

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

#    ReadTempThread(TempDelay,CSVPath,ClientID,client,)

    Temp = threading.Thread(target=ReadTempThread, \
            args=(TempDelay,CSVPath,ClientID,client,), name='Temp', daemon=True)
    Temp.start()
    CPU = threading.Thread(target=ReadCPUThread, \
            args=(CPUDelay,CSVPath,ClientID,client,), name='CPU', daemon=True)
    CPU.start()
    Disk = threading.Thread(target=ReadDiskThread, \
            args=(DiskDelay,CSVPath,ClientID,client,), name='Disk', daemon=True)
    Disk.start()
    Load = threading.Thread(target=ReadLoadThread, \
            args=(LoadDelay,CSVPath,ClientID,client,), name='Load', daemon=True)
    Load.start()
    Wifi = threading.Thread(target=ReadWifiThread, \
            args=(WifiDelay,CSVPath,ClientID,client,), name='Wifi', daemon=True)
    Wifi.start()
    SerialGPIO = threading.Thread(target=ReadGPIOData, \
             args=(CSVPath,ClientID,client,), name='SerialGPIO', daemon=True)
    SerialGPIO.start()
    SerialUSB = threading.Thread(target=ReadUSBData, \
             args=(CSVPath,ClientID,client,), name='SerialUSB', daemon=True)
    # SerialUSB.start()

    Run_flag = True
#    ThreadAll = threading.enumerate()
#    ProcessError(CSVPath, 'Threads', '', 'Running:'+str(ThreadAll), ThreadAll )
    while Run_flag:
        try:  # catch a <CTRL C>
#            Threads = {}
#            for ThreadName in ['Temp', 'CPU', 'Wifi', 'Serial']:
#                Threads[ThreadName]=ThreadName
#            print (Threads )
#            Running=''
#            for ThreadName in ThreadAll :
#                if ThreadName.isAlive():
#                    Running = Running+';'+ThreadName.getName()
#                else:
#                    ProcessError(CSVPath, 'Threads', '', 'Restarted:'+ThreadName.getName(), Running )
#            print (Running) # debug
#            ProcessError(CSVPath, 'Threads', '', 'Running:'+str(Running), Running )
            time.sleep(3000000)
        except KeyboardInterrupt:
            Run_flag=False # Stop the loop

print('\n','Exiting app')       # Send a cheery message

time.sleep(4)          # Four seconds to allow sending to finish

