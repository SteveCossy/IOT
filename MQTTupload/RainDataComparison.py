#!/usr/bin/env python
import csv, os, requests
import xml.etree.cElementTree as ET
import pandas as pd
import plotly.tools
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
init_notebook_mode()

# ------------------------ Steve's material begins -----------------------------
# Convert XML file to CSV
# Based on http://blog.appliedinformaticsinc.com/how-to-parse-and-convert-xml-to-csv-using-python/
# Steve Cosgrove's play pen - last updated 18 May 2018
# Data APIs from https://drive.google.com/open?id=0B9SezXULrAGFQkZwbjVkZkcwNTJYZmVXSXNGUVphOVlHc1Zr
# Get a list of sites that have rainfall:
# http://hilltop.gw.govt.nz/data.hts?Service=Hilltop&Request=SiteList&Location=Yes&Measurement=Rainfall
# Puat a site name into this URL to get the XML file:
# wget "http://hilltop.gw.govt.nz/data.hts?Service=Hilltop&Request=GetData&Site=Makara Stream at Quartz Hill Wind Farm&Measurement=Rainfall&From=10/4/2018&To=17/5/2018"

#filename_base = 'MS-QH-Rain_10-04-2018_17-05-2018' # this line and the bottom two line do not work with 'requests' module
# filename_ext_in = '.xml'
# filename_ext_out = '.csv'
# tree = ET.parse(filename_base+filename_ext_in)
# root = tree.getroot()
# # open a file for writing
# Rainfall_data = open(filename_base+filename_ext_out, 'w')
# ------------------------ Steve's material ends -----------------------------

# ------------------------ Elaine Wei modified some of Steve's codes ---------
# ------------------------ Codes are adopted from Python modules' documentations.
# ------------------------ Part 1: extracting data via Internet,
# -------------------------        saving into xml file,
# -------------------------        converting to csv file.
# ----- ensuring uniqueness of csv file name -----
try:
     csvfile = open(os.path.expanduser(r"makara.csv"),"w")
except:
    os.remove(os.path.expanduser(r"makara.csv"))
    csvfile = open(os.path.expanduser(r"makara.csv"),"w")

# ----- get data via browser -----
url = 'http://hilltop.gw.govt.nz/data.hts?Service=Hilltop&Request=GetData&Site=Makara Stream at Quartz Hill Wind Farm&Measurement=Rainfall&From=4/9/2018&To=5/9/2018&interval=1%20hour"'
filesource = requests.get(url)

with open("makara.xml","wb") as xmlfile:   # ----- write data into xml file
    xmlfile.write(filesource.content)
xmlfile='makara.xml'                        # ----- parse xmlfile
csvfile='makara.csv'

tree = ET.parse(xmlfile)
root = tree.getroot()

Rainfall_data = open('makara.csv','w')   # ----- write data into csv file

csvwriter = csv.writer(Rainfall_data)               # ----- create the csv writer object
Rainfall = []                                       # ----- create a list to hold csv data
csvwriter.writerow(Rainfall)
Rainfall.append('Timestamp')                        # ----- set list header in csv
Rainfall.append('Datavalue')
csvwriter.writerow(Rainfall)
for times in root.findall('./Measurement/Data/'):   # ----- search for specific string in xmlfile
        time = times[0].text
        value = times[1].text
        Rainfall = []                               # ----- extract each element value from xmlfile
        Rainfall.append(time)
        Rainfall.append(value)
        csvwriter.writerow(Rainfall)
Rainfall_data.close()
os.remove(os.path.expanduser(r"makara.xml"))        # ----- delete xml file after finish writing csv file

# ------ second csv file ------

try:
     csvfile2 = open(os.path.expanduser(r"makara2.csv"),"wb")
except:
    os.remove(os.path.expanduser(r"makara2.csv"))
    csvfile2 = open(os.path.expanduser(r"makara2.csv"),"wb")

# ----- get data via browser -----

url2 = 'http://hilltop.gw.govt.nz/data.hts?Service=Hilltop&Request=GetData&Site=Kaiwharawhara%20Stream%20at%20Karori%20Reservoir&Measurement=Rainfall&From=04/09/2018&To=05/09/2018&interval=1%20hour"'
filesource2 = requests.get(url2)

with open('makara2.xml', 'wb') as xmlfile2:   # ----- write data into xml file
    xmlfile2.write(filesource2.content)
xmlfile2='makara2.xml'                        # ----- parse xmlfile
csvfile2='makara2.csv'


tree2 = ET.parse(xmlfile2)
root2 = tree2.getroot()

Rainfall_data2 = open('makara2.csv','w')   # ----- write data into csv file

csvwriter2 = csv.writer(Rainfall_data2)               # ----- create the csv writer object
Rainfall2 = []                                       # ----- create a list to hold csv data
csvwriter2.writerow(Rainfall2)
Rainfall2.append('Timestamp')                        # ----- set list header in csv
Rainfall2.append('Datavalue')
csvwriter2.writerow(Rainfall2)
for times2 in root2.findall('./Measurement/Data/'):   # ----- search for specific string in xmlfile
        time2 = times2[0].text
        value2 = times2[1].text
        Rainfall2 = []                               # ----- extract each element value from xmlfile
        Rainfall2.append(time2)
        Rainfall2.append(value2)
        csvwriter2.writerow(Rainfall2)
Rainfall_data2.close()
os.remove(os.path.expanduser(r"makara2.xml"))        # ----- delete xml file after finish writing cs

# ------------------------ end of part 1 -----------------------------

# ------------------------ Part 2: visualising data ------------------

with open('makara.csv','r') as f1:
    reader1 = csv.reader(f1)
# --- convert column from csv to array begins
colnames = ['time', 'value']
data = pd.read_csv('makara.csv', names=colnames)
time = data.time.tolist()
value = data.value.tolist()

# --- dataset 2
with open('makara2.csv','r') as f2:
    reader2 = csv.reader(f2)

# --------------------get column from csv to be array begins --------------
colnames2 = ['time', 'value']
data2 = pd.read_csv('makara2.csv', names=colnames2)
time2 = data2.time.tolist()
value2 = data2.value.tolist()

# --- read data by using pandas library
plotly.offline.init_notebook_mode(connected=True)
df = pd.read_csv("makara.csv")
df2=pd.read_csv("makara2.csv")
# --- read data by using pandas library
plotly.offline.init_notebook_mode(connected=True)
df = pd.read_csv("makara.csv")
df2=pd.read_csv("makara2.csv")

#--- draw plot 1
trace0 = plotly.graph_objs.Scatter(
    x=time,
    y=value,
    line = dict(color = 'red')
)

#--- draw plot2
trace1 = plotly.graph_objs.Scatter(
    x=time2,
    y=value2,
    line=dict(color = 'blue')
)

# --- place two plots into two positions
fig = plotly.tools.make_subplots(rows=2,cols=1)

fig.append_trace(trace0,2,1)
fig.append_trace(trace1,1,1)
# --- name title, axises
fig['layout'].update(title='Rain Data Comparison')
fig['layout']['yaxis1'].update(title='Karori rainfall level\n(mm)')
fig['layout']['yaxis2'].update(title='Makara rainfall level\n(mm)')

fig['layout']['xaxis1'].update(title='Timestamp')
fig['layout']['xaxis2'].update(title='Timestamp')

# --- display chart as html file
plotly.offline.iplot(fig)
plotly.offline.plot(fig,filename='RainComparison')

# ----- extract data from csv file
#  ----------------- Double plots ends -------------------
