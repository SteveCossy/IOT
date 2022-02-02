"""
Some Constants that are passed as a dictionary to make it a single common source for any changes made.
"""

# Create and return the dictionary
def ReturnDict():
    ConstantDict = {\
        'HomeDir'  : os.environ['HOME'] \
        'ConfFile' : '/MQTTConfig.txt' \
        'CSVPath'  : HomeDir+'/' \
        'CSV' 	   : '.csv' \
        'CrLf' 	   : '\r\n' \
        'CSVTopic' : 'RSSILatLong' \
        'Eq'	   : ' = ' \
        'Qt'	   : '"'}

    return ConstantDict