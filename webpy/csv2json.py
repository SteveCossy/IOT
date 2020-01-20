# csv2jason.py
# from https://stackoverflow.com/questions/48586647/python-script-to-convert-csv-to-geojson
# started 17 November 2019
# modified to take csv from command line 19 Dec 2019
# modified to encapsulate main logic into function 31 Dec 2019

import csv, sys, os, json, webbrowser
from collections import OrderedDict

# InputPath ='./archive.old'
# InputPath ='/home/cosste/CayMQTT/'
# OutputPath='/var/www/html/OSM/temp/'
# OutputPath='./temp/'

#if (InputFile.endswith('.csv')) :
#    OutputFile = os.path.join(OutputPath,InputFile[:-4])

# InputFile  = os.path.join(InputPath,InputFile)
# OutputFile = OutputFile+'.geojason'

# InputFile =  '/home/cosste/CayMQTT/RSSILatLong.csv'
# OutputFile = '/var/www/html/OSM/RSSILatLong.geojson'

# https://stackoverflow.com/questions/4188467/how-to-check-if-an-argument-from-commandline-has-been-set


# print( 'Getting '+InputFile )

# os.system('scp 192.168.196.71:/home/cosste/RSSILatLong.csv '+InputFile)
# Got get the csv file from the computer where it is created

# Turn this into a function that can be imported from another script -SP
def to_geojson(InputFile, OutputFile):
    """Convert CSV file to GeoJSON"""

    li = []
    with open(InputFile, 'r') as CsvFile:
    #    dialect = csv.Sniffer().sniff(CsvFile.read(1024))
        reader = csv.reader(CsvFile, delimiter=',')
        next(reader) # skip header
    #    reader = csv.reader(CsvFile, dialect)
#        for TIME,RSSI,LAT,LONG  in reader:
        for TIME,LATwhole,LAT,LONGwhole,LONG  in reader:
            d = OrderedDict()
            d['type'] = 'Feature'
            d['properties'] = {
                'TimeStamp': TIME,
#                'RSSI': RSSI,
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

# This code only gets called when the file is called on the command line
# It does not run if imported into another script -SP
if __name__ == '__main__':
    InputFile=str(sys.argv[1])
    OutputFile=str(sys.argv[2]) # This is currently a full path and filename
    to_geojson(InputFile, OutputFile)
