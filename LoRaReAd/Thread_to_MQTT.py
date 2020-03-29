# Based on ideas from: https://realpython.com/intro-to-python-threading/
# Steve Cosgrove 28 March 2020
import logging
import threading
import time
import os
import sys
import cayenne.client
import datetime
from SensorLib import GetWirelessStats
from SensorLib import GetSerialData
from MQTTUtils import Save2Cayenne
from MQTTUtils import Save2CSV
from MQTTUtils import ProcessError
from MQTTUtils import DataError
from MQTTUtils import ReadTemp
from gpiozero  import CPUTemperature

# the IOT/LoRaReAd dir contains MQTTUtils.py
# MQTTUpath =     os.path.join(HomeDir,'IOT/LoRaReAd')
# sys.path.append(MQTTUpath)

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
TempDelay =	2 
CPUDelay =	6
WifiDelay =	12

# Set up logging and local copies of data
ConfPathFile = os.path.join(HomeDir, AUTH_FILE)

LogPathFile  = os.path.join(CSVPath, LOG_FILE)
logging.basicConfig(filename=LogPathFile, level=logging.DEBUG)
CurrentTime = datetime.datetime.now().isoformat()
logging.debug(CrLf+'***** Starting at: {a}'.format(a=CurrentTime)+' *****' )

# The callback for when a message is received from Cayenne.
def on_message(client, userData, message):
# based on https://developers.mydevices.com/cayenne/docs/cayenne-mqtt-api/#cayenne-mqtt-api-mqtt-messaging-topics-send-actuator-updated-value
#    global COUNTER
    print("message received: " ,str(message.payload.decode("utf-8")))

def on_connect(client, userData, flags, rc):
    print("Connected with result code "+str(rc))

# Connect to Cayenne Cloud
client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.on_connect = on_connect

client.begin(CayenneParam.get('CayUsername'), \
   CayenneParam.get('CayPassword'), \
   CayenneParam.get('CayClientID'), \
   )


def ReadTempThread(Freq):
  while True :
    Value = ReadTemp()
    logging.info("Temp Loop: %s", Value)
    time.sleep(Freq)

def ReadCPUThread(Freq):
  while True :
    Value = CPUTemperature().temperature
    logging.info("CPU  Loop: %s", Value)
    time.sleep(Freq)

def ReadWifiThread(Freq):
  while True :
    Value = GetWirelessStats()
    logging.info("Wifi Loop: %s", Value)
    time.sleep(Freq)

def ReadSerialData(client):
  #   Define the PicAxe Divisors
  DivisorDict = dict.fromkeys(string.ascii_uppercase)
  for key in DivisorDict :
      DivisorDict[key] =	1
  DivisorDict['A'] =	10 # Soil Moisture
  DivisorDict['B'] =	10 # Temperature

  while True :
    Value = GetSerialData()
    logging.info("Serial Loop: %s", Value)
    Channel = Value["Channel"]
    Data = Value["Data"]
    Status = Value["Status"]
    ClientID = Value["ClientID"]
    Error = Value["Error"]
    Save2Cayenne (client, 'Stat', Status, 1)
    if Status == 0 :
        Save2CSV (CSVPath, ClientID, 'Error', Error)
    else :
        # Status is OK, so write the data ...
        Save2CSV (CSVPath, ClientID, Channel, Data)
        Save2Cayenne (client, Channel, Data, DivisorDict[Channel])

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    Temp = threading.Thread(target=ReadTempThread, args=(TempDelay,), daemon=True)
    Temp.start()
    CPU = threading.Thread(target=ReadCPUThread, args=(CPUDelay,), daemon=True)
    CPU.start()
    Wifi = threading.Thread(target=ReadWifiThread, args=(WifiDelay,), daemon=True)
    Wifi.start()

    Run_flag = True
    while Run_flag:
        try:  # catch a <CTRL C>
            time.sleep(1000000000)
        except KeyboardInterrupt:
            Run_flag=False # Stop the loop

print('\n','Exiting app')       # Send a cheery message

time.sleep(4)          # Four seconds to allow sending to finish

