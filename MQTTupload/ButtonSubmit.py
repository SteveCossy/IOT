import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

url1Start = 'http://hilltop.gw.govt.nz/data.hts?Service=Hilltop&Request=GetData&Site=Makara Stream at Quartz Hill Wind Farm&Measurement=Rainfall&From='
url2Start = 'http://hilltop.gw.govt.nz/data.hts?Service=Hilltop&Request=GetData&Site=Kaiwharawhara%20Stream%20at%20Karori%20Reservoir&Measurement=Rainfall&From='
urlMid = '&To='
urlEnd = '&interval=1%20hour'

app = dash.Dash()
app.layout = html.Div([

    html.Hr(),
    html.Br(),html.Br(),
    html.Label('From:   '),
    dcc.Input(id='input1',type = 'date',value = ''),
    html.Label('To :   '),
    dcc.Input(id='input2',type = 'date',value = ''),

    html.Button('Submit',id='btnSubmit',type = 'submit'),
    html.Div(id='output')
])

    # download that works
    # ----- get data via browser -----
    # url = 'http://hilltop.gw.govt.nz/data.hts?Service=Hilltop&Request=GetData&Site=Makara Stream at Quartz Hill Wind Farm&Measurement=Rainfall&From=4/9/2018&To=5/9/2018&interval=1%20hour"'
    # filesource = requests.get(url)

@app.callback(
    Output('output', 'children'),
    [Input('btnSubmit', 'n_clicks')],
    state=[State('input1', 'value'),
     State('input2', 'value')
     ])

def show(n_clicks, input1, input2):
    sep = '/'
    startDate = input1[0:4]+sep+input1[5:7]+sep+input1[8:10]
    endDate = input2[0:4]+sep+input2[5:7]+sep+input2[8:10]
    url1 = url1Start+startDate+urlMid+endDate+urlEnd
    url2 = url2Start+startDate+urlMid+endDate+urlEnd
    return 'A = {}, B = {}, URL1 = {} & URL2 = {}'.format(
    startDate, endDate, url1, url2
    )
if __name__ == '__main__':
    app.run_server(debug=True)
