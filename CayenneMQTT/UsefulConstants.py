"""
Some Constants that are passed as a dictionary to make it a single common source for any changes made.
"""

import os
HomeDir = os.environ['HOME']

# Create and return the dictionary
def ReturnDict():
    ConstantDict = {\
        'HomeDir'  : HomeDir, \
        'ConfFile' : '/MQTTConfig.txt', \
        'CSVPath'  : HomeDir+'/', \
        'CSV' 	   : '.csv', \
        'CrLf' 	   : '\r\n', \
        'CSVTopic' : 'RSSILatLong', \
        'Eq'	   : ' = ', \
        'Qt'	   : '"'}

    return ConstantDict