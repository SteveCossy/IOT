# MQTT-Utils.py
# library of routines to assist with using getting IoT data, 
# then using MQTT protocol to manipulate it,
# particularly for use in the Cayenne Cloud.
# Consolidated from https://github.com/SteveCossy/IOT
# Started 09 Jan 2020 by Steve Cosgrove

import csv, sys, os, json, webbrowser, time, datetime, logging, string
from collections import OrderedDict

def HelpMessage():
   print("You need help!  Try https://github.com/SteveCossy/IOT/wiki")

def ProcessError(CSVPath, ClientID, CayClient, CSV_Message, Message):
# Save Message to a file and Cayenne
#    global LastError
    CurrentTime = datetime.datetime.now().isoformat()
    CSVPathFile = Save2CSV (CSVPath, ClientID, 'Exception', CSV_Message)
    CurrentTime = datetime.datetime.now().isoformat()
    LogPathFile = logging.getLoggerClass().root.handlers[0].baseFilename
#    print (LastError, '********' )
#    ErrorTime = datetime.datetime.now()
#    ErrorGap    = ErrorTime - LastError['time']
#    if ErrorGap.days > 0: # Ages since last error
#        Continue = True
#        ResetCount = True
#    elif ErrorGap.seconds > LastError['period']: # OK time since last error
#        Continue = True
#        ResetCount = True
#    elif LastError['count'] < LastError['threshold']: # Still counting
#        LastError['count'] += 1
#        Continue = True
#        ResetCount = False
#    else:      # We have a problem
    Continue = False
#        ResetCount = True
        
#    if ResetCount:
#        LastError = {
#            'time'  : ErrorTime,
#            'count' : 0
#        }

#    if not(Continue):
#        Message = Message+' terminating thread'
        
    logging.exception(Message)
    os.system('tail -20 '+LogPathFile) # display last error if in foreground
    if CayClient :
        Save2Cayenne (CayClient, 'Stat', -1, 1)

    return(Continue)

def DegMin2DegDeci(Location,Direction):
# Change Degrees.Minutes to Degrees.DecimalPartOfDegrees
# Location is a Degrees.Minutes float
# Direction is North South East or West
    Whole,Deci = divmod(Location,1)
    DecDeci = Whole+( Deci / 0.60 )
    if Direction == 'E' or Direction == 'N':
        DecDeci *= -1
    return (DecDeci)

def PiSerial ():
# Preference is a string saying whether our preference is tty or USBx
# Assumes tehre will only be one onboard serial port
# Based on https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
# ... and https://stackoverflow.com/questions/54288475/pyserial-module-serial-has-no-attribute-tools/54288652
# ... and https://pyserial.readthedocs.io/en/latest/tools.html
# GPIO serial port is not detected. See https://github.com/SteveCossy/IOT/wiki/Serial-Port-Use
# https://raspberrypi.stackexchange.com/questions/45570/how-do-i-make-serial-work-on-the-raspberry-pi3-or-later-model/45571#45571

    from serial.tools import list_ports

    Ports = list_ports.comports(include_links=False)
    Devices = {}

    for Port in Ports :
        Device = Port.device
        if ('USB' in Device):
            USBnbr = Device[-4:]
            Devices[USBnbr] = Device
#        else:
#            Devices['Onboard'] = Device  Always returns /dev/ttyAMA0 no not helpful
    return Devices

def DataError(Device, Channel, textMessage, PacketIn):
    CrLf = '\r\n'
    print ("Device: ",Device,CrLf \
        ,"Channel: ",Channel,CrLf \
        ,"Message: ",textMessage,CrLf \
        ,"Packet Recieved: '"+str(PacketIn)+"'" \
        )

def Save2CSV (CSVPath, Device, Channel, Data):
# CSVPath String: is folder for the file (filename to be made from device & channel)
# Device is a unique ID. Perhaps the very long Cayenne Device ID
# Channel unique letter used to distiguish different sensors on same device
#   ref https://github.com/SteveCossy/IOT/wiki/Tables-defining:-Cayenne-Data-Channels---PicAxe-Channels---Cicadacom
# Data what we are going to write.

#    import datetime
    CurrentTime	= datetime.datetime.now().isoformat()
    CSV		= '.csv'
    CSVFile	= str(Device)+"_"+str(Channel)+CSV
    CrLf 	= '\r\n'
    CSVPathFile	= os.path.join(CSVPath, CSVFile)
    FIELDNAMES	= ['time','device','data']

    DATALIST = {'time':CurrentTime,
		'device':Device,
		'data':Data
		}
    print ( 'Save2CSV', DATALIST )
    # Needs thinking about further - test type, as it could also be a list

    if not os.path.isfile(CSVPathFile):
    # There is not currently an output file
        print ("Creating new output file: "+CSVPathFile)
        if not os.path.exists(CSVPath):
            os.mkdir(CSVPath)
        with open(CSVPathFile, 'w') as CSVFile:
            writer = csv.DictWriter(CSVFile, fieldnames=FIELDNAMES)
            writer.writeheader()
    with open(CSVPathFile, 'a') as CSVFile:
        writer = csv.DictWriter(CSVFile, fieldnames=FIELDNAMES)
        writer.writerow(DATALIST)
    return CSVPathFile


def Save2Cayenne (client, Channel, Data, Divisor):
# Client is an open MQTT client object
# Channel is the Cayenne channel letter for the data
# Data is a data type appropriate for that type of channel
# ref https://github.com/SteveCossy/IOT/wiki/Tables-defining:-Cayenne-Data-Channels---PicAxe-Channels---Cicadacom

#   Define the PicAxe Channels
    ChannelMap = dict.fromkeys(string.ascii_uppercase)	# Keys are 'A' 'B' 'C' 'D'
    for key in ChannelMap :
        ChannelMap[key]		= ord(key)-64		# A=1 B=2 etc

#   Add other arbatory Channels
    ChannelMap['CPUtemp']	= 41
    ChannelMap['Stat']		= 40
    ChannelMap['ExtTemp']	= 47
    ChannelMap['WifiLvl']	= 46
    ChannelMap['WifiLnk']	= 45
    ChannelMap['DiskAvg']	= 44
    ChannelMap['LoadAvg']	= 43

    print ( 'Save2Cayenne', Channel+':(',ChannelMap[Channel],')' \
            , 'Data:', Data )

    if Channel in ChannelMap:
        Data = Data / Divisor
        client.virtualWrite( ChannelMap[Channel], Data, "analog_sensor", "null")
    else:
        print( "********* Channel "+Channel+" not found! **************")
    client.loop()
    
def to_geojson(InputFile, OutputFile):
    """Convert CSV file to GeoJSON"""

    li = []
    with open(InputFile, 'r') as CsvFile:
    #    dialect = csv.Sniffer().sniff(CsvFile.read(1024))
        reader = csv.reader(CsvFile, delimiter=',')
        next(reader) # skip header
    #    reader = csv.reader(CsvFile, dialect)
        for TIME,RSSI,LAT,LONG  in reader:
            d = OrderedDict()
            d['type'] = 'Feature'
            d['properties'] = {
                'TimeStamp': TIME,
                'RSSI': RSSI,
                'Lat' : LAT,
                'Long': LONG
            }
            d['geometry'] = {
                'type': 'Point',
                'coordinates': [float(LONG), float(LAT)]
    #            'coordinates': [Latitude, Longitude]
            }
            li.append(d)

    # print( 'Writing '+OutputFile )

    d = OrderedDict()
    d['type'] = 'FeatureCollection'
    d['features'] = li
    with open(OutputFile, 'w') as f:
        f.write(json.dumps(d, sort_keys=False, indent=4))

# webbrowser.open('http://net-informations.com', new=2)

# NewURL = 'http://students.pcsupport.ac.nz/OSM/?'+OutputFile
# os.system("echo "+NewURL+" >NewURL.url")
# webbrowser.open(NewURL, new=2)

# This script is not intended to be called on the command line.
# If it is called that way, then it will give a help message and exit
if __name__ == '__main__':
    HelpMessage()
