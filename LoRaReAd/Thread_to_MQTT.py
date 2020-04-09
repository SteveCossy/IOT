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
import cayenne.client, datetime, time, serial, logging, csv, os, requests, datetime, time, glob, uuid, sys, toml, struct, traceback, string
from SensorLib import GetWirelessStats
from SensorLib import GetSerialData
from MQTTUtils import Save2Cayenne
from MQTTUtils import Save2CSV
from MQTTUtils import DataError
from MQTTUtils import ReadTemp
from MQTTUtils import ProcessError
from gpiozero  import CPUTemperature

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
  while True :
    Value = ReadTemp()
#    logging.info("Temp Loop: %s", Value)
    Channel = 'ExtTemp'
    Save2CSV (CSVPath, ClientID, Channel, Value)
    Save2Cayenne (client, Channel, Value, 1)
    time.sleep(Freq)

def ReadCPUThread(Freq,CSVPath,ClientID,client):
  while True :
    Value = CPUTemperature().temperature
#    logging.info("CPU  Loop: %s", Value)
    Channel = 'CPUtemp'
    Save2CSV (CSVPath, ClientID, Channel, Value)
    Save2Cayenne (client, Channel, Value, 1)
    time.sleep(Freq)

def ReadWifiThread(Freq,CSVPath,ClientID,client):
  while True :
    Value = GetWirelessStats()
#    logging.info("Wifi Loop: %s", Value)
    Link = Value['wlan0']['link']
    Channel = 'WifiLnk'
    Save2CSV (CSVPath, ClientID, Channel, Link)
    Save2Cayenne (client, Channel, Link, 100)
    Level = Value['wlan0']['level']
    Channel = 'WifiLvl'
    Save2CSV (CSVPath, ClientID, Channel, Level)
    Save2Cayenne (client, Channel, Level, 100)
    time.sleep(Freq)

def ReadSerialData(CSVPath,ClientID,client):
  #   Define the PicAxe Divisors
  DivisorDict = dict.fromkeys(string.ascii_uppercase)
  for key in DivisorDict :
      DivisorDict[key] =	1
  DivisorDict['A'] =	10 # Soil Moisture
  DivisorDict['B'] =	10 # Temperature
  DivisorDict['S'] =	10 # Kihi-02 Moisture
  DivisorDict['T'] =	10 # Kihi-02 Temperature

  while True :
      try :
        Value = GetSerialData(CSVPath,ClientID)
    #    logging.info("Serial Loop: %s", Value)
        Channel = Value["Channel"]
        Data = Value["Data"]
        Status = Value["Status"]
        ClientID = Value["ClientID"]
        Error = Value["Error"]
        Save2Cayenne (client, 'Stat', Status, 1)
    #    logging.info("Wifi Loop: %s", Value)
        if Status == 0 :
            Save2CSV (CSVPath, ClientID, 'Error', Error)
        else :
            # Status is OK, so write the data ...
            Save2CSV (CSVPath, ClientID, Channel, Data)
            Save2Cayenne (client, Channel, Data, DivisorDict[Channel])
      except :
          Message = "Exception reading LoRa Data"
          CSV_Message = Message
          ProcessError(CSVPath, ClientID, '', CSV_Message, Message)

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
    CPUDelay =	60
    WifiDelay =	300

    # Set up logging and local copies of data
    ConfPathFile = os.path.join(HomeDir, AUTH_FILE)
    LogPathFile  = os.path.join(CSVPath, LOG_FILE)
    
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename=LogPathFile, format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")
    # logging.basicConfig(filename=LogPathFile, level=logging.DEBUG)
    CurrentTime = datetime.datetime.now().isoformat()
    logging.debug(CrLf+'***** Starting at: {a}'.format(a=CurrentTime)+' *****' )

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
    Wifi = threading.Thread(target=ReadWifiThread, \
            args=(WifiDelay,CSVPath,ClientID,client,), name='Wifi', daemon=True)
    Wifi.start()
    Serial = threading.Thread(target=ReadSerialData, \
             args=(CSVPath,ClientID,client,), name='Serial', daemon=True)
    Serial.start()

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

