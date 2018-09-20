import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash()
app.layout = html.Div([

    html.Hr(),
    html.Br(),html.Br(),
    html.Label('From    '),
    dcc.Input(id='input1',type = 'date',value = ''),

    html.Label('To    '),
    dcc.Input(id='input2',type = 'date',value = ''),

    html.Button('Submit',id='btnSubmit',type = 'submit'),
    html.Div(id='output')
    # download that works
    # ----- get data via browser -----
    # url = 'http://hilltop.gw.govt.nz/data.hts?Service=Hilltop&Request=GetData&Site=Makara Stream at Quartz Hill Wind Farm&Measurement=Rainfall&From=4/9/2018&To=5/9/2018&interval=1%20hour"'
    # filesource = requests.get(url)
   

])

@app.callback(
    Output('output', 'children'),
    [Input('btnSubmit', 'n_clicks')],
    state=[State('input1', 'value'),
     State('input2', 'value')
     ])
def show(n_clicks, input1, input2):
    startDate = input1.replace('-', '/')
    return 'A = {}, B = {}'.format(
        startDate, input2
    )
if __name__ == '__main__':
    app.run_server(debug=True)
