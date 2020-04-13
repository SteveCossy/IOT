# Based on ideas from: https://realpython.com/intro-to-python-threading/
# Steve Cosgrove 28 March 2020

import os
import sys
from PrintArg import printarg

HomeDir =       os.environ['HOME']
# the IOT/LoRaReAd dir contains MQTTUtils.py
MQTTUpath =     os.path.join(HomeDir,'IOT/LoRaReAd')
sys.path.append(MQTTUpath)
from MQTTUtils import ProcessError


def TestFunk():
#    global LastError
    print( LastError['time'], 'FirstFunc ********************' )
    printarg()

# Set up timer for catching repeated errors
LastError = {
    'time'  : 'Now',
    'count' : 0,
    'period' : 300, # Time to keep counting 300 seconds = 5 minutes
    'threshold' : 3 # Look for 3 errors in 5 minutes
}

TestFunk()

