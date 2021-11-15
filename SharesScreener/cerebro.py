# -*- coding: utf-8 -*-
"""
Created on Fri May 21 22:45:39 2021

@author: LK
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 21 22:17:52 2021

@author: LK
"""

import matplotlib
import backtrader as bt
import backtrader.feeds as btfeeds
import datetime
import pandas as pd

# Specify paths so packages can be imported from other directories
import sys
sys.path.insert(0,r'C:\Users\LK\Documents\GitHub\CryptoAI\assets')
from strategies import MA_CrossOver

# Modify datafeed so that csv can be imported

data = btfeeds.GenericCSVData(
    dataname='ohlc_df_1d.csv',
    fromdate=datetime.datetime(2020, 1, 1),
    todate=datetime.datetime(2020, 12, 31),
    nullvalue=0.0,
    dtformat=('%Y-%m-%dT%H:%M:%S'),
    datetime=1,
    open=3,
    high=4,
    low=5,
    close=6,
    volume=-1,
    openinterest=-1,
    reverse=False
)


# Initiate the Cerebro instance

cerebro = bt.Cerebro()

# Change the available cash in the beginning

cerebro.broker.set_cash(100000)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Add the datafeed to the Cerebro instance

cerebro.adddata(data)

# Specify the strategy 

cerebro.addstrategy(MA_CrossOver)
      
# Run over everything

cerebro.run()

# Display the results

cerebro.plot()

# Print out the final result

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())