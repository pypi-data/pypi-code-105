import os
import numpy as np
import matplotlib.pyplot as plt

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
# import plotly.express as px

from flame_dash import isml
caller = isml.loadmpi() 
caller.loadFile("/home/shubham/strial/mixinglayer.1.2400E-04.field.mpi") #default data??
options = caller.options #not defined in isml
function = caller.change #not defined in isml



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='heatmap'),
    dcc.Dropdown(
        id='Choose-Variable',
        options=[{'label': k, 'value': v} for k,v in options.items()],
        value = list(options.values())[0]
    ),
    dcc.Slider(
        id='TimeStepRange',
        min=0,
        max=19,
        step=1,
        value=10,
    )
])

@app.callback(
    Output('heatmap', 'figure'),
    [Input('Choose-Variable', 'value')])
def update_figure(var):
    fig = function(var)    
    return fig


if __name__ == '__main__':
    app.run_server()
