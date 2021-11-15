# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 21:05:33 2021

@author: LK
"""

import san
import datetime
import matplotlib.pyplot as plt
import mplfinance as fplt
import pandas as pd
import numpy as np
import yfinance as yf

# Define timeframe and interval

timeframe_weeks = 40

# Calculate start and end date

end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(weeks=timeframe_weeks)


# Access Bitcoin Price (High/Low/Close)

daily_high_price_bitcoin = san.get(
    "daily_high_price_usd/bitcoin",
    from_date=start_date,
    to_date=end_date,
    interval="1d"
)

daily_low_price_bitcoin = san.get(
    "daily_low_price_usd/bitcoin",
    from_date=start_date,
    to_date=end_date,
    interval="1d"
)

daily_closing_price_bitcoin = san.get(
    "daily_closing_price_usd/bitcoin",
    from_date=start_date,
    to_date=end_date,
    interval="1d"
)

daily_open_price_bitcoin = san.get(
    "daily_opening_price_usd/bitcoin",
    from_date=start_date,
    to_date=end_date,
    interval="1d"
)

# Create dataframe of prices

daily_prices = pd.concat([daily_open_price_bitcoin, daily_high_price_bitcoin, daily_low_price_bitcoin, daily_closing_price_bitcoin], axis=1)
daily_prices.columns = ['Open', 'High', 'Low', 'Close']

# Display price in candlestick chart

fplt.plot(
    daily_prices,
    type='candle',
    style='charles',    
    title='Price of Bitcoin over time')

# Calculate daily returns based on closing Price

daily_returns_bitcoin = pd.DataFrame({'BTC': daily_prices['Close'].pct_change().dropna()})

# Plot return distribution

plt.hist(daily_returns_bitcoin['BTC'], bins=10)
plt.show()

# Compute daily and annual volatility

daily_returns_bitcoin_volatility = daily_returns_bitcoin.std()
yearly_returns_bitcoin_volatility = daily_returns_bitcoin_volatility * np.sqrt(365)



