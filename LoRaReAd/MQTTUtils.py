# MQTT-Utils.py
# library of routines to assist with using getting IoT data, 
# then using MQTT protocol to manipulate it,
# particularly for use in the Cayenne Cloud.
# Consolidated from https://github.com/SteveCossy/IOT
# Started 09 Jan 2020 by Steve Cosgrove

import csv, sys, os, json, webbrowser, time, datetime, logging
from collections import OrderedDict

def HelpMessage():
   print("You need help!  Try https://github.com/SteveCossy/IOT/wiki")

def ProcessError(CSVPath, ClientID, CayClient, CSV_Message, Message):
# Save Message to a file and Cayenne
# Return False to stop excecution
    print ( Message )
    Save2CSV (CSVPath, ClientID, 'Exception', CSV_Message)
    CurrentTime = datetime.datetime.now().isoformat()
    logging.exception(Message + ' ' + CurrentTime)
    Save2Cayenne (CayClient, 'Stat', -1)

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

    from serial.tools import list_ports

    Ports = list_ports.comports(include_links=False)
    Devices = {}

    for Port in Ports :
        Device = Port.device
        if ('USB' in Device):
            USBnbr = Device[-4:]
            Devices[USBnbr] = Device
        else:
            Devices['Onboard'] = Device
    return Devices
            





def Save2CSV (CSVPath, Device, Channel, Data):
# CSVPath String: is folder for the file (filename to be made from device & channel)
# Device is a unique ID. Perhaps the very long Cayenne Device ID
# Channel unique letter used to distiguish different sensors on same device
#   ref https://github.com/SteveCossy/IOT/wiki/Tables-defining:-Cayenne-Data-Channels---PicAxe-Channels---Cicadacom
# Data what we are going to write.

    import datetime
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
    print ( DATALIST )
    # Needs thinking about further - test type, as it could also be a list

    if not os.path.isfile(CSVPathFile):
    # There is not currently an output file
        print ("Creating new output file: "+CSVPathFile)
        with open(CSVPathFile, 'w') as CSVFile:
            writer = csv.DictWriter(CSVFile, fieldnames=FIELDNAMES)
            writer.writeheader()
    with open(CSVPathFile, 'a') as CSVFile:
        writer = csv.DictWriter(CSVFile, fieldnames=FIELDNAMES)
        writer.writerow(DATALIST)


def Save2Cayenne (client, Channel, Data):
# Client is an open MQTT client object
# Channel is the Cayenne channel letter for the data
# Data is a data type appropriate for that type of channel
# ref https://github.com/SteveCossy/IOT/wiki/Tables-defining:-Cayenne-Data-Channels---PicAxe-Channels---Cicadacom

      print (Channel, Data)

      if Channel == 'A':
        Data = float(Data)/10
        if Data < 60000:
          client.virtualWrite(1, Data, "analog_sensor", "null")
 
      elif Channel == 'B':
        Data = float(Data)/1
        if Data < 60000:
          client.virtualWrite(2, Data, "analog_sensor", "null")
 
      elif Channel == 'C':
        Data = float(Data)/1
        if Data < 5000:
          client.virtualWrite(3, Data, "analog_sensor", "null")
 
      elif Channel == 'D':
        Data = float(Data)/1
        if Data < 500:
          client.virtualWrite(4, Data, "analog_sensor", "null")
 
      elif Channel == 'E':
        Data = float(Data)/1
        if Data < 5000:
          client.virtualWrite(5, Data, "analog_sensor", "null")
 
      elif Channel == 'F':
        Data = float(Data)/1
        if Data < 5000:
          client.virtualWrite(6, Data, "analog_sensor", "null")
 
      elif Channel == 'G':
        Data = float(Data)/1*-1
        if Data < 256:
          client.virtualWrite(7, Data, "analog_sensor", "null")
 
      elif Channel == 'H':
        Data = float(Data)/60000
        if Data < 65325:
          client.virtualWrite(8, Data, "analog_sensor", "null")
 
      elif Channel == 'I':
        Data = float(Data)/1
        if Data < 256:
          client.virtualWrite(9, Data, "analog_sensor", "null")
 
      elif Channel == 'J':
        Data = float(Data)/60000
        if Data < 65325:
          client.virtualWrite(10, Data, "analog_sensor", "null")
 
      elif Channel == 'K':
        Data = float(Data)/256
        if Data < 65535:
          client.virtualWrite(11, Data, "analog_sensor", "null")
 
      elif Channel == 'L':
        Data = float(Data)/1
        if Data < 65335:
          client.virtualWrite(12, Data, "analog_sensor", "null")
 
      elif Channel == 'M':
        Data = float(Data)/1
        if Data < 500:
          client.virtualWrite(13, Data, "analog_sensor", "null")
 
      elif Channel == 'N':
        Data = float(Data)/1
        if Data < 500:
          client.virtualWrite(14, Data, "analog_sensor", "null")
 
      elif Channel == 'O':
        Data[0] = Data[0]
        if Data < 500:
          client.virtualWrite(15, Data, "analog_sensor", "null")
 
      elif Channel == 'P':
        Data = float(Data)/1
        if Data < 500:
          client.virtualWrite(16, Data, "analog_sensor", "null")
 
      elif Channel == 'Q':
        Data = float(Data)/1
        if Data < 500:
          client.virtualWrite(17, Data, "analog_sensor", "null")
 
      elif Channel == 'R':
        Data = float(Data)/1
        if Data < 500:
          client.virtualWrite(18, Data, "analog_sensor", "null")
 
      elif Channel == 'S':
        Data = float(Data)/1
        if Data < 500:
          client.virtualWrite(19, Data, "analog_sensor", "null")
 
      elif Channel == 'T':
        Data = float(Data)/1
        if Data < 500:
          client.virtualWrite(20, Data, "analog_sensor", "null")
 
      elif Channel == 'U':
        Data = float(Data)/1
        if Data < 500:
          client.virtualWrite(21, Data, "analog_sensor", "null")
 
      elif Channel == 'V':
        Data = float(Data)/1
        if Data < 500:
          client.virtualWrite(22, Data, "analog_sensor", "null")
 
      elif Channel == 'W':
        Data = float(Data)/10
        client.virtualWrite(23, Data, "analog_sensor", "null")

      elif Channel == 'X':
        Data = float(Data)/1
        client.virtualWrite(24, Data, "analog_sensor", "null")

      elif Channel == 'Y':
        Data = float(Data)/1
        client.virtualWrite(25, Data, "analog_sensor", "null")

      elif Channel == 'Z':
        Data = float(Data)/1
        client.virtualWrite(26, Data, "analog_sensor", "null")

      elif Channel == 'Stat':
#        Data = float(Data)/1
        client.virtualWrite(40, Data, "analog_sensor", "null")

      else:
        print( "Channel "+Channel+" not found!")


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
