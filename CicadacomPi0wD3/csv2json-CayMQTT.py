# csv2jason.py
# from https://stackoverflow.com/questions/48586647/python-script-to-convert-csv-to-geojson
# started 17 November 2019

import csv, sys, os, json
from collections import OrderedDict

# InputFile=str(sys.argv[1])
# outputfile=str(sys.argv[2])

InputFile =  '/home/cosste/CayMQTT/CicadacomPi0wD3.csv'
OutputFile = '/var/www/html/CPi/CicadacomPi0wD3.geojson'

print( 'Getting '+InputFile )

# remote command  python3 /home/cosste/IOT/CicadacomPi0wD3/cayMQTT_to_csv.py
os.system('scp 192.168.196.71:/home/cosste/CicadacomPi0wD3.csv '+InputFile)
# Got get the csv file from the computer where it is created

li = []
with open(InputFile, 'r') as CsvFile:
#    dialect = csv.Sniffer().sniff(CsvFile.read(1024))
    reader = csv.reader(CsvFile, delimiter=',')
    next(reader) # skip header
#    reader = csv.reader(CsvFile, dialect)
    for TIME,BAT,LAT,LONG  in reader:
        d = OrderedDict()
        d['type'] = 'Feature'
        d['properties'] = {
            'TimeStamp': TIME,
            'Bat': BAT,
            'Lat' : LAT,
            'Long': LONG
        }
        d['geometry'] = {
            'type': 'Point',
            'coordinates': [float(LONG), float(LAT)]
#            'coordinates': [Latitude, Longitude]
        }
        li.append(d)

print( 'Writing '+OutputFile )

d = OrderedDict()
d['type'] = 'FeatureCollection'
d['features'] = li
with open(OutputFile, 'w') as f:
    f.write(json.dumps(d, sort_keys=False, indent=4))
