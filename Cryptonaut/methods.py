# -*- coding: utf-8 -*-
"""
Created on Mon May 24 19:29:51 2021

@author: LK
"""

import talib
import cryptowatch as cw
import numpy.random as nr
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objs as go
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.model_selection as ms
import sklearn.metrics as sklm
from sklearn import preprocessing
from sklearn import linear_model
import math
import scipy.stats as ss
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html


def get_candle(pair):
    
    ohlc_all_timeframes = cw.markets.get(F"{pair}", ohlc=True)
    
    # Create empty dataframe for 1h candlestick
    
    ohlc_df_1h = pd.DataFrame(columns = ['Timestamp','Datetime','Candle', 'Open', 'High', 'Low', 'Close'])
    
     # Store 1h candlestick data in dataframe
     
    ohlc_1h = ohlc_all_timeframes.of_1h
    
    counter_1h = np.arange(len(ohlc_1h))
    
    for i in counter_1h:
            
        ohlc_df_1h.loc[i,'Timestamp'] = ohlc_1h[:][i][0]
        ohlc_df_1h.loc[i,'Datetime'] = datetime.datetime.fromtimestamp(ohlc_1h[:][i][0]).isoformat()
        ohlc_df_1h.loc[i,'Candle'] = '1h'
        ohlc_df_1h.loc[i,'Open'] = ohlc_1h[:][i][1]
        ohlc_df_1h.loc[i,'High'] = ohlc_1h[:][i][2]
        ohlc_df_1h.loc[i,'Low'] = ohlc_1h[:][i][3]
        ohlc_df_1h.loc[i,'Close'] = ohlc_1h[:][i][4]
        
    # Create empty dataframe for 4h candlestick
    
    ohlc_df_4h = pd.DataFrame(columns = ['Timestamp','Datetime','Candle', 'Open', 'High', 'Low', 'Close'])
    
     # Store 4h candlestick data in dataframe
     
    ohlc_4h = ohlc_all_timeframes.of_4h
    
    counter_4h = np.arange(len(ohlc_4h))
    
    for i in counter_4h:
            
        ohlc_df_4h.loc[i,'Timestamp'] = ohlc_4h[:][i][0]
        ohlc_df_4h.loc[i,'Datetime'] = datetime.datetime.fromtimestamp(ohlc_4h[:][i][0]).isoformat()        
        ohlc_df_4h.loc[i,'Candle'] = '4h'
        ohlc_df_4h.loc[i,'Open'] = ohlc_4h[:][i][1]
        ohlc_df_4h.loc[i,'High'] = ohlc_4h[:][i][2]
        ohlc_df_4h.loc[i,'Low'] = ohlc_4h[:][i][3]
        ohlc_df_4h.loc[i,'Close'] = ohlc_4h[:][i][4]
    
    # Create empty dataframe for 1d candlestick
    
    ohlc_df_1d = pd.DataFrame(columns = ['Timestamp','Datetime','Candle', 'Open', 'High', 'Low', 'Close'])
    
     # Store 1d candlestick data in dataframe
     
    ohlc_1d = ohlc_all_timeframes.of_1d
    
    counter_1d = np.arange(len(ohlc_1d))
    
    for i in counter_1d:
            
        ohlc_df_1d.loc[i,'Timestamp'] = ohlc_1d[:][i][0]
        ohlc_df_1d.loc[i,'Datetime'] = datetime.datetime.fromtimestamp(ohlc_1d[:][i][0]).isoformat()        
        ohlc_df_1d.loc[i,'Candle'] = '1d'
        ohlc_df_1d.loc[i,'Open'] = ohlc_1d[:][i][1]
        ohlc_df_1d.loc[i,'High'] = ohlc_1d[:][i][2]
        ohlc_df_1d.loc[i,'Low'] = ohlc_1d[:][i][3]
        ohlc_df_1d.loc[i,'Close'] = ohlc_1d[:][i][4]    
          
    # Create empty dataframe for 1w candlestick
    
    ohlc_df_1w = pd.DataFrame(columns = ['Timestamp','Datetime','Candle', 'Open', 'High', 'Low', 'Close'])
    
     # Store 1w candlestick data in dataframe
     
    ohlc_1w = ohlc_all_timeframes.of_1w
    
    counter_1w = np.arange(len(ohlc_1w))
    
    for i in counter_1w:
            
        ohlc_df_1w.loc[i,'Timestamp'] = ohlc_1w[:][i][0]
        ohlc_df_1w.loc[i,'Datetime'] = datetime.datetime.fromtimestamp(ohlc_1w[:][i][0]).isoformat()        
        ohlc_df_1w.loc[i,'Candle'] = '1w'
        ohlc_df_1w.loc[i,'Open'] = ohlc_1w[:][i][1]
        ohlc_df_1w.loc[i,'High'] = ohlc_1w[:][i][2]
        ohlc_df_1w.loc[i,'Low'] = ohlc_1w[:][i][3]
        ohlc_df_1w.loc[i,'Close'] = ohlc_1w[:][i][4]    
     
        
    
    return ohlc_df_1h, ohlc_df_4h, ohlc_df_1d, ohlc_df_1w

def add_return(df):
    
    # Calculate Absolute Return per Candle
    df['Abs_Return'] = df.Close - df.Open
    
    # Calculate relative Return measured in pips per candle
    
    for row in np.arange(len(df)):
        try:
            df.loc[row,'Rel_Return_pips'] = (df.loc[row,'Close'] - df.loc[row,'Open']) / df.loc[row,'Open'] * 100 * 100
        except: 
            df.loc[row,'Rel_Return_pips'] = 0
    
    
    for row in np.arange(len(df)-1):
        df.loc[0,'Cum_Return'] = df.loc[0,'Abs_Return']
        df.loc[row+1,'Cum_Return'] = df.loc[row,'Cum_Return'] + df.loc[row+1,'Abs_Return']


    
    #df['Rel_Return_pips'] = ((df.Close-df.Open)/df.Open) * 100 * 100
    
    return df


def add_indicators(df,t_sma,t_ema,t_adx,t_rsi,n_dev_dn,n_dev_up,t_bbands):
    
    # Add SMA
    df[f'SMA_{t_sma}'] = talib.SMA(df['Close'], timeperiod=t_sma)
    
    # Add EMA
    df[f'EMA_{t_ema}'] = talib.EMA(df['Close'], timeperiod=t_ema)
    
    # Add ADX    
    df[f'ADX_{t_adx}'] = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=t_adx)
    
   
    # Add RSI
    df[f'RSI_{t_rsi}'] = talib.RSI(df['Close'], timeperiod=t_rsi)
    
    # Add BBANDS
       
    upper, mid, lower = talib.BBANDS(df['Close'], nbdevup=n_dev_up, nbdevdn=n_dev_dn, timeperiod=t_bbands)
    
    df['bband_up'] = upper
    df['bband_mid'] = mid
    df['bband_low'] = lower   
    
    
    df = df.dropna()

    df = df.reset_index(drop=True)
    
    # Add Interpretation to ADX Values

    for candle in np.arange(len(df)):
        if df.loc[candle,F'ADX_{t_adx}'] < 25:
            df.loc[candle,'ADX_Trend'] = 'No Trend'
        elif df.loc[candle,F'ADX_{t_adx}'] < 50:
            df.loc[candle,'ADX_Trend'] = 'Trend'
        else:
            df.loc[candle,'ADX_Trend'] = 'Strong Trend'
        
  # Add Interpretation to RSI Values

    for candle in np.arange(len(df)):
        if df.loc[candle,F'RSI_{t_rsi}'] < 30:
            df.loc[candle,'RSI_Trend'] = 'Oversold'
        elif df.loc[candle,F'RSI_{t_rsi}'] < 70:
            df.loc[candle,'RSI_Trend'] = 'Neutral'
        else:
            df.loc[candle,'RSI_Trend'] = 'Overbought'                  
        
    return df


def split_df(S,df):
    N = int(len(df)/S)
    frames = [ df.iloc[i*S:(i+1)*S].copy() for i in range(N+1) ]
    return frames

def create_cs_fig(df):
    chart = go.Candlestick(x=df['Datetime'], 
                   open=df['Open'],
                   high=df['High'],
                   low=df['Low'],
                   close=df['Close']
                   )
    fig = go.Figure(data=[chart])
    return fig

def plot_box(df, x, y, hue):
    sns.set_style("whitegrid")
    sns.boxplot(x, y,hue=hue, data=df)
    plt.xlabel(x) # Set text for the x axis
    plt.ylabel(y)# Set text for y axis
    plt.show()
    
    
def hist_plot(vals, lab):
    ## Distribution plot of values
    sns.distplot(vals)
    plt.title('Histogram of ' + lab)
    plt.xlabel('Value')
    plt.ylabel('Density')


def print_metrics(y_true, y_predicted, n_parameters):
    ## First compute R^2 and the adjusted R^2
    r2 = sklm.r2_score(y_true, y_predicted)
    r2_adj = r2 - (n_parameters - 1)/(y_true.shape[0] - n_parameters) * (1 - r2)
    
    ## Print the usual metrics and the R^2 values
    print('Mean Square Error      = ' + str(sklm.mean_squared_error(y_true, y_predicted)))
    print('Root Mean Square Error = ' + str(math.sqrt(sklm.mean_squared_error(y_true, y_predicted))))
    print('Mean Absolute Error    = ' + str(sklm.mean_absolute_error(y_true, y_predicted)))
    print('Median Absolute Error  = ' + str(sklm.median_absolute_error(y_true, y_predicted)))
    print('R^2                    = ' + str(r2))
    print('Adjusted R^2           = ' + str(r2_adj))

def hist_resids(y_test, y_score):
    ## first compute vector of residuals. 
    resids = np.subtract(y_test.reshape(-1,1), y_score.reshape(-1,1))
    ## now make the residual plots
    sns.distplot(resids)
    plt.title('Histogram of residuals')
    plt.xlabel('Residual value')
    plt.ylabel('count')
    

def resid_qq(y_test, y_score):
    ## first compute vector of residuals. 
    resids = np.subtract(y_test.reshape(-1,1), y_score.reshape(-1,1))
    ## now make the residual plots
    ss.probplot(resids.flatten(), plot = plt)
    plt.title('Residuals vs. predicted values')
    plt.xlabel('Predicted values')
    plt.ylabel('Residual')
 
def resid_plot(y_test, y_score):
    ## first compute vector of residuals. 
    resids = np.subtract(y_test.reshape(-1,1), y_score.reshape(-1,1))
    ## now make the residual plots
    sns.regplot(y_score, resids, fit_reg=False)
    plt.title('Residuals vs. predicted values')
    plt.xlabel('Predicted values')
    plt.ylabel('Residual')

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
    