# Based on ideas from: https://realpython.com/intro-to-python-threading/
# Steve Cosgrove 28 March 2020
import logging
import threading
import time
import os
import sys
from ParseProcNet import GetWirelessStats


HomeDir =       os.environ['HOME']
# the IOT/LoRaReAd dir contains MQTTUtils.py
MQTTUpath =     os.path.join(HomeDir,'IOT/LoRaReAd')
sys.path.append(MQTTUpath)
from MQTTUtils import Save2CSV
from MQTTUtils import ReadTemp
from gpiozero  import CPUTemperature


TempDelay =	2 # Seconds between reading each value
CPUDelay =	6
WifiDelay =	12

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

