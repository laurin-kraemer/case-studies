# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 23:26:16 2021

@author: LK
"""
from datetime import datetime
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define API 
api_adresses = 'https://api.glassnode.com/v1/metrics/addresses/count?a=btc&i=1w&api_key=89374d03-d8fe-4f96-a075-cc40732b9597'

# Package, sent and catch the response
r = requests.get(api_adresses)

# Extract data from the response 
api_adresses_data = r.json()

# Create empty DataFrame
adresses_data = pd.DataFrame()

# Store data in the DataFrame
for i in np.arange(len(api_adresses_data)):
    adresses_data.loc[i, 'Time'] = datetime.utcfromtimestamp(api_adresses_data[i]['t'])
    adresses_data.loc[i, 'Total Adresses'] = api_adresses_data[i]['v']
    
adresses_data.set_index('Time', inplace=True)

plt.plot(adresses_data['Total Adresses'])
plt.title('Number of Adresses over time')
plt.show()


