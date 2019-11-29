# Create TOML configuration file for Cayenne MQTT interation
# Steve Cosgrove - started 25 Nov 2019
# based on https://pypi.org/project/toml/

import toml, uuid, sys, os

# Useful constants
Eq	= ' = '
CrLf	= '\r\n'
Qt	= '"'
HomeDir =    os.environ['HOME']
# HomeDir =      '/home/pi'
CsvPath =      HomeDir+'/'
CSV =           '.csv'

CayenneFile	= HomeDir+'/cayenneMQTT.txt'

ConfigFile = toml.load(CayenneFile)
CayenneParam = ConfigFile.get('cayenne')
print (CayenneParam)

for key,val in CayenneParam.items():
    print( key, "=>", val )

# for name in dir():
#    myvalue = eval(name)
#    print( name, "is", type(name), "and is equal to ", myvalue )
