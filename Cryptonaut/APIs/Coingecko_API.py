# -*- coding: utf-8 -*-
"""
Created on Tue May 18 12:29:06 2021

@author: LK
"""

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

# Get current price

current_price = cg.get_price(ids='bitcoin', vs_currencies='usd')

# Get list of all tokens

token_list = cg.get_coins_list()

# Get detailed data about specific currency

bitcoin_data = cg.get_coin_by_id('bitcoin')

# Get historical data

hist_data = cg.get_coin_history_by_id('bitcoin', date='10-10-2020')

# Get historical market data (including price)

hist_market_data = cg.get_coin_market_chart_by_id('bitcoin', days=1, vs_currency = 'usd')

# Get Open, High, Low, Close

ophlc = cg.get_coin_ohlc_by_id('bitcoin', days=1, vs_currency='usd')



