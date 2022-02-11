"""
This File is no longer needed
"""

# Initialise the temperature threshold file
# This file is used for error detection and penguin dectection algorithms in SensorLib

import toml, uuid, sys, os

# Useful constants
# Directly from MkAuthSettings
Eq	= ' = '
CrLf	= '\r\n'
Qt	= '"'
HomeDir =    os.environ['HOME']
# HomeDir =      '/home/pi'
CsvPath =      HomeDir+'/'
CSV =           '.csv'

ThresholdFile = HomeDir+'/thresholds.txt'

# Sets the increase threshold to a user-set number
# Used for fine-tuning in case of diffent species or environments and for initial set-up
DetectThreshk   = 'DetectThresh'+Eq
DetectThreshd   = Qt+str(sys.argv[1])+Qt

# Sets the difference threshold to a user-set number
ErrThreshk      = 'ErrThresh'+Eq
ErrThreshd      = Qt+str(sys.argv[2])+Qt

Opening         = '# Threshold values to determine how and when the Error dectection and penguin detection algorithms are tripped'
DetectSection   = '[detectThresh]'
ErrSection      = '[errThresh]'      
Closing         = '# Thiis file was created by '+str(sys.argv[0])

TomlString = Opening+CrLf \
    +DetectSection+CrLf \
    +DetectThreshk+DetectThreshd+CrLf \
    +ErrSection+CrLf \
    +ErrThreshk+ErrThreshd+CrLf \
    +Closing

ParsedToml = toml.loads(TomlString)

OutFile = open(ThresholdFile, "w")
toml.dump(ParsedToml, OutFile)
OutFile.close