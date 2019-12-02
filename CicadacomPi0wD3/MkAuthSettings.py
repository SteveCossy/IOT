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

# Get machines MAC address to use for a unique ClientID
MAC = hex(uuid.getnode())
# Returns 14 characters 0xMMMMMMMMMMMM

CayenneUserk	= "CayUsername"+Eq
CayenneUserd	= Qt+str(sys.argv[1])+Qt

CayennePassk	= "CayPassword"+Eq
CayennePassd	= Qt+str(sys.argv[2])+Qt

CayenneClIDk	= "CayClientID"+Eq
CayenneClIDd	= Qt+str(sys.argv[3])+Qt

CayenneFile	= HomeDir+'/CicadacomPi0wD3.txt'

Opening  = '# Authentication settings to connect to Cayenne'
Section  = '[cayenne]'
UniqueIDk = 'UniqueID'+Eq
UniqueIDd = Qt+'CicadacomPi0wD3'+MAC+Qt
Closing  = '# This file was created by '+str(sys.argv[0])

TomlString = Opening+CrLf \
	+Section+CrLf \
	+CayenneUserk + CayenneUserd+CrLf \
	+CayennePassk + CayennePassd+CrLf \
	+CayenneClIDk + CayenneClIDd+CrLf \
	+UniqueIDk + UniqueIDd+CrLf \
	+Closing
# print (TomlString, CayenneFile)

ParsedToml = toml.loads(TomlString)
# FileContents = toml.dumps(ParsedToml)
# print (FileContents)

OutFile = open(CayenneFile, "w" )
toml.dump(ParsedToml, OutFile)
OutFile.close


