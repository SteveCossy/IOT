# csv2jason.py
# from https://stackoverflow.com/questions/48586647/python-script-to-convert-csv-to-geojson
# started 17 November 2019

import csv, sys
import json
from collections import OrderedDict

inputfile=str(sys.argv[1])
outputfile=str(sys.argv[2])

li = []
with open(inputfile, 'r') as csvfile:
#    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    reader = csv.reader(csvfile, delimiter=',')
    next(reader) # skip header
#    reader = csv.reader(csvfile, dialect)
    for RSSI,Longitude,Latitude  in reader:
        d = OrderedDict()
        d['type'] = 'Feature'
        d['properties'] = {
            'Area_Name': RSSI
        }
        d['geometry'] = {
            'type': 'Point',
            'coordinates': [float(Latitude), float(Longitude)]
#            'coordinates': [Latitude, Longitude]
        }
        li.append(d)

d = OrderedDict()
d['type'] = 'FeatureCollection'
d['features'] = li
with open(outputfile, 'w') as f:
    f.write(json.dumps(d, sort_keys=False, indent=4))
