"""
Some Constants that are passed as a dictionary to make it a single common source for any changes made.
"""
import os

# Create and return the dictionary
def ReturnDict():
    ConstantDict = {
        'HomeDir'  : os.environ['HOME'],
        'ConfFile' : '/MQTTConfig.txt',
        'CSV' 	   : '.csv',
        'CrLf' 	   : '\r\n',
        'CSVTopic' : 'RSSILatLong',
        'Eq'	   : ' = ',
        'Qt'	   : '"'
	}

    ConstantDict['CSVPath'] = ConstantDict['HomeDir'] + '/',

    return ConstantDict
