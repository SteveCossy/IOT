
#!/usr/bin/env python
import csv, os, requests
import xml.etree.cElementTree as ET
import pandas as pd
from dash.dependencies import Input, Output,State
import dash
import dash_html_components as html
import dash_core_components as dcc

# ------------------------ Elaine Wei modified some of Steve's codes ---------
# ------------------------ Codes are adopted from Python modules' and plotly dash's documentations.
# ------------------------ App includes :   extracting data via Internet,
# -------------------------                 saving into xml file,
# -------------------------                 converting to csv file,
# -------------------------                 visulising data on web page via plotly dash.
# ------------------------- App purposes:   customising date range to see different graphs,
# -------------------------                 downloading graph as png file,
# -------------------------                 downloading csv file.



# ----- app begins -----

url1Start = 'http://hilltop.gw.govt.nz/data.hts?Service=Hilltop&Request=GetData&Site=Makara Stream at Quartz Hill Wind Farm&Measurement=Rainfall&From='
url2Start = 'http://hilltop.gw.govt.nz/data.hts?Service=Hilltop&Request=GetData&Site=Kaiwharawhara%20Stream%20at%20Karori%20Reservoir&Measurement=Rainfall&From='
urlMid = '&To='
urlEnd = '&interval=1%20hour'
app = dash.Dash()
app.title = 'Rain Data of Wellington West'
colors = {
    'background': '#111111',
    'text': '#1a001a'
}
app.layout = html.Div(
    html.Div([
        html.H1(children = 'Makara and Karori rain data',style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        html.P('IOT allows people connecting devices to make them meeting specific purpose of accessing and storing data with ease.',style={
        'textAlign': 'center',
        'color': colors['text']
    }),

        html.Div(children = 'Date Range'),
        html.Br(),
        html.Label('From:'),
        html.Label('        '),
        dcc.Input(id='input1',value='',type='date'),

        html.Label('            '),
        html.Label('To:'),
        html.Label('        '),
        dcc.Input(id='input2', value='', type='date',),

        html.Label('            '),
        html.Button('Submit',id='btnSubmit',type='submit'),

        html.Div(id='output-graph')

    ]))

# ----- clicking on submit button to return graph with defined date range -----
@app.callback(

    Output('output-graph', 'children'),
    [Input('btnSubmit', 'n_clicks')],
    state=[State('input1', 'value'),
     State('input2', 'value')
     ]
)

def update_graph(n_clicks, input1, input2):
    sep = '/'
    startDate = input1[0:4] + sep + input1[5:7] + sep + input1[8:10]
    endDate = input2[0:4] + sep + input2[5:7] + sep + input2[8:10]
    url1 = url1Start + startDate + urlMid + endDate + urlEnd
    url2 = url2Start + startDate + urlMid + endDate + urlEnd
    # ----- ensuring uniqueness of csv file name -----
    try:
        csvfile = open(os.path.expanduser(r"makara.csv"), "w")
    except:
        os.remove(os.path.expanduser(r"makara.csv"))
        csvfile = open(os.path.expanduser(r"makara.csv"), "w")

    # ----- get data via browser -----
    filesource = requests.get(url1)

    with open("makara.xml","wb") as xmlfile:            # ----- write data into xml file
        xmlfile.write(filesource.content)
    xmlfile='makara.xml'                                # ----- parse xmlfile
    csvfile='makara.csv'

    tree = ET.parse(xmlfile)
    root = tree.getroot()

    Rainfall_data = open('makara.csv','w')              # ----- write data into csv file

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
         csvfile2 = open(os.path.expanduser(r"karori.csv"),"wb")
    except:
        os.remove(os.path.expanduser(r"karori.csv"))
        csvfile2 = open(os.path.expanduser(r"karori.csv"),"wb")

    # ----- get data via browser -----

    filesource2 = requests.get(url2)

    with open('karori.xml', 'wb') as xmlfile2:          # ----- write data into xml file
        xmlfile2.write(filesource2.content)
    xmlfile2 = 'karori.xml'  # ----- parse xmlfile
    csvfile2 = 'karori.csv'

    tree2 = ET.parse(xmlfile2)
    root2 = tree2.getroot()

    Rainfall_data2 = open('karori.csv', 'w')            # ----- write data into csv file

    csvwriter2 = csv.writer(Rainfall_data2)             # ----- create the csv writer object
    Rainfall2 = []  # ----- create a list to hold csv data
    csvwriter2.writerow(Rainfall2)
    Rainfall2.append('Timestamp')                       # ----- set list header in csv
    Rainfall2.append('Datavalue')
    csvwriter2.writerow(Rainfall2)
    for times2 in root2.findall('./Measurement/Data/'): # ----- search for specific string in xmlfile
        time2 = times2[0].text
        value2 = times2[1].text
        Rainfall2 = []                                  # ----- extract each element value from xmlfile
        Rainfall2.append(time2)
        Rainfall2.append(value2)
        csvwriter2.writerow(Rainfall2)
    Rainfall_data2.close()
    os.remove(os.path.expanduser(r"karori.xml"))        # ----- delete xml file after finish writing cs

    # --- convert column from csv to array begins
    with open('makara.csv', 'r') as f1:
        reader1 = csv.reader(f1)

    colnames = ['time', 'value']
    data = pd.read_csv('makara.csv', names=colnames)
    time = data.time.tolist()
    value = data.value.tolist()

    # --- dataset 2
    with open('karori.csv', 'r') as f2:
        reader2 = csv.reader(f2)

    # --- get column from csv to be array begins
    colnames2 = ['time', 'value']
    data2 = pd.read_csv('karori.csv', names=colnames2)
    time2 = data2.time.tolist()
    value2 = data2.value.tolist()

    # --- return outcome of function ---
    return dcc.Graph(
        id='makara_karori',
        figure = {
            'data': [
                {'x':time, 'y': value, 'type': 'line', 'name':'Makara','mode': 'lines','marker':{'color':'red'}},
                {'x':time,'y': value,'type': 'line','name':'Makara','mode': 'markers','line':{'color':'red','dash':'dashdot'}},

                {'x':time2, 'y': value2, 'name':'Karori','mode': 'lines','line':{'color':'blue','width':1}},
                {'x':time2, 'y': value2, 'type': 'line', 'name':'Karori','mode': 'markers','marker':{'color':'blue'}}
            ],

            'layout':{
                'title':'Rain Comparison',
                'xaxis':dict(
                    title = 'Timestamp\n(hourly)',
                    titlefont=dict(
                        size = 18,
                        color='#360556'
                    )),
                'yaxis':dict(
                    title = 'Rain level\n(mm)',
                    titlefont=dict(
                        size = 18,
                        color='#360556'
                ))
            }
        }
    )

# --- debug app ---
if __name__ == '__main__':
    app.run_server(debug=True)
