# -*- coding: utf-8 -*-
"""
Created on Sun May 30 22:31:55 2021

@author: LK
"""
# Import packages

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

from methods import get_candle, create_cs_fig, generate_table, add_return, add_indicators

# Define CSS Properties

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

"""

Prepare data 

"""


# Get data 

candles = get_candle('kraken:btcusd')

# Extract tuple

candle_1h = candles[0]
candle_4h = candles[1]
candle_1d = candles[2]
candle_1w = candles[3]

# Add Returns to df

candle_1h = add_return(candle_1h)
candle_4h = add_return(candle_4h)
candle_1d = add_return(candle_1d)
candle_1w = add_return(candle_1w)

# Add indicators to df

# Momentum
t_sma = 20
t_ema = 30

# Strength of Trend
t_adx = 20

# Oversold/Overbought
t_rsi = 10

# BBands
n_dev_dn = 2
n_dev_up = 2
t_bbands = 20

candle_1h = add_indicators(candle_1h, t_sma,t_ema,t_adx,t_rsi,n_dev_dn,n_dev_up,t_bbands)
candle_4h = add_indicators(candle_4h, t_sma,t_ema,t_adx,t_rsi,n_dev_dn,n_dev_up,t_bbands)
candle_1d = add_indicators(candle_1d, t_sma,t_ema,t_adx,t_rsi,n_dev_dn,n_dev_up,t_bbands)
candle_1w = add_indicators(candle_1w, t_sma,t_ema,t_adx,t_rsi,n_dev_dn,n_dev_up,t_bbands)

# Combine / Concat the dataframes

candles = pd.concat([candle_1h, candle_4h, candle_1d, candle_1w])

# Find out Available timeframes

available_candles = candles['Candle'].unique()

"""

Create Charts to Visualize Data 

"""
# Candlestick Chart   

chart_fig = create_cs_fig(candles)

# Bollinger Band with Closing Price

fig_indicators = make_subplots(rows=3, cols=1,subplot_titles=('1','2','3','4'))


"""

Create Dash instance and define layout

"""

test = [{'label': i, 'value': i} for i in available_candles]

# Create dash instance

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# Define Layout

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='candle_timeframe',
                options=[{'label': i, 'value': i} for i in available_candles],
                value='candle'
            )
            
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='dropdown_indicator',
                options=[
                    {'label': 'SMA', 'value': 'SMA'},
                    {'label': 'EMA', 'value': 'EMA'}
                    ],
                value=['SMA', 'EMA'],
                multi=True
            )  
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

     dcc.Graph(
            id = 'price_data',
            figure = chart_fig,
            responsive=True
            ),
     
      dcc.Graph(
            id = 'indicators',
            figure = fig_indicators,
            responsive=False
            )
])


"""

Make the Chart interactive:
    
    - Create Callback
    - Define Functions to update Chart

"""

@app.callback(
    Output('price_data', 'figure'),
    Input('candle_timeframe', 'value'),
    )


def update_graph(candle_timeframe):
    candles_copy = candles[candles['Candle']==candle_timeframe]
    
    fig = create_cs_fig(candles_copy)

    return fig

@app.callback(
    Output('indicators', 'figure'),
    Input('dropdown_indicator', 'value'),
    Input('candle_timeframe', 'value')
    )

def update_indicator_chart(dropdown_indicator,candle_timeframe):
    candles_copy = candles[candles['Candle']==candle_timeframe]
    trace = go.Scatter(x=candles_copy['Datetime'], y=candles_copy['RSI_10'], mode='lines', name=f'RSI_{t_rsi}')
    fig_indicators.add_trace(trace, row = 1, col = 1)
    return fig_indicators

if __name__ == "__main__":
    app.run_server(debug=True)