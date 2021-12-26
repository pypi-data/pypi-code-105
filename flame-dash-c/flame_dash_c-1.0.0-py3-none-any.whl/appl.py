#import os  #unused??
#import numpy as np  #unused??
# import matplotlib.pyplot as plt
#import plotly.express as px  #unused??

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from flame_dash import isml #it is a internal module
import base64

encoded_image = base64.b64encode(open('C:/Users/Dell/Downloads/python_data_sets/data1/aset/temp.png', 'rb').read())

caller = isml.loadmpi() 
caller.loadFile("data1") #hcci is a dataset file
var = caller.variables

# from hcci import species as options
# from hcci import selSpec,selTime


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = 'FlameLab'
app.layout = html.Div([
    dcc.Dropdown(
        id='datasets',
        options=[{'label': l, 'value': l} for l in ['hcci','isml']],
        value = 'hcci'
    ),
    dcc.Tabs(id="tabs",value='tab-1',children=[
        dcc.Tab(label="interactive",value='tab-1',children=[
            html.H2('Slow Interactive Graph'),
            dcc.Graph(id='heatmap')
            ]),
        dcc.Tab(label="static",value='tab-2',children=[
            html.H3('Fast Static Graph'),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), id='imshow')
            ])
#     html.Img(src=impath+'temp.png', id='imshow'),
    ]),
    dcc.Dropdown(
        id='variables',
        options=[{'label': k, 'value': v} for k,v in var.items()],
        value = list(var.values())[0]
    ),
    dcc.Slider(
        id='TimeStepRange',
        min=0,
        max=19,
        step=1,
        value=10,
    ),
    html.Button('Submit',id='button')
])


@app.callback(
     Output('variables', 'options'),
     Output('TimeStepRange','max'),
    [Input('datasets', 'value')])
def update_output(i):
    caller.loadFile(i)
    n = len(caller.flist)
    return [{'label': k, 'value': v} for k,v in caller.variables.items()],n

@app.callback(
    Output('heatmap', 'figure'),
    [Input('button','n_clicks')],
    [State('TimeStepRange','value')])
def update_fig(n,t):
    caller.selTime(t)
    fig = caller.dyPlot()
    return fig
  

@app.callback(
#     Output('heatmap', 'figure'),
    Output('imshow', 'src'),
    [Input('button','n_clicks'),
    Input('TimeStepRange', 'value'),
    Input('variables', 'value')])
def update_fig(n,t,j):
    caller.selTime(t)    
    caller.selSpec(j)    
    fig = caller.stPlot()
    encoded= base64.b64encode(open('C:/Users/Dell/Downloads/python_data_sets/data1/aset/temp.png', 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())
#     return fig

if __name__ == '__main__':
 app.run_server()
##app.run_server(host='10.24.50.67',port='9031',debug=True)
