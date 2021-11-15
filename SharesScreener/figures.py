# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 19:19:00 2021

@author: LK
"""


import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

from methods import get_candle, create_cs_fig, generate_table, add_return, add_indicators

def create_cs_fig(df):
    chart = go.Candlestick(x=df['Datetime'], 
                   open=df['Open'],
                   high=df['High'],
                   low=df['Low'],
                   close=df['Close']
                   )
    fig = go.Figure(data=[chart])
    return fig


# Get data 

candles = get_candle('kraken:btcusd')
pio.renderers.default='browser'

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

# Filter Dataframe

start_date = '01-01-2019'
candle1d = candle_1d.loc[(pd.to_datetime(candle_1d.Datetime) >start_date)]

# Create Figure

fig = make_subplots(rows=3, cols=1,shared_xaxes=True,)


# Add Row 1 | Column 1
fig.add_trace(
    go.Scatter(name='Price',x=candle1d['Datetime'], y=candle1d['Close']),
    row=1, col=1, 
)

fig.add_trace(
    go.Scatter(x=candle1d['Datetime'], y=candle1d['bband_up']),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=candle1d['Datetime'], y=candle1d['bband_low']),
    row=1, col=1
)



fig.update_layout(
    title="Plot Title",
    xaxis_title="Price",
    yaxis_title="Datetime",
    legend_title="Legend Title",
    height=800,
    width=1200,
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
fig.show()






# Plotly figure 2
#fig2 = go.Figure(fig.add_traces(
           #      data=px.line(df_ame_gdp_top5, x='year', y='gdpPercap',
        #                      color="country",
                   #           line_group="country", line_dash='country', hover_name="country")._data))

# Add Closing Price (Traces not showing up correctly)
close_trace = go.Scatter(x=candle_1d['Datetime'], y=candle_1d['Close'])
fig_indicators = fig_indicators.add_trace(close_trace,row=1,col=1)

upperband_trace = go.Scatter(x=candle_1d['Datetime'], y=candle_1d['bband_up'])
fig_indicators.add_trace(close_trace,row=1,col=1)

middleband_trace = go.Scatter(x=candle_1d['Datetime'], y=candle_1d['bband_mid'])
fig_indicators.add_trace(close_trace,row=1,col=1)

lowerband_trace = go.Scatter(x=candle_1d['Datetime'], y=candle_1d['bband_low'])
fig_indicators.add_trace(close_trace,row=1,col=1)

