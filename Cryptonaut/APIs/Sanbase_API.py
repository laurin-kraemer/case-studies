# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 20:11:05 2021

@author: LK
"""

import san
import datetime

# Projects in the space

projects_df = san.get("projects/all")

# Active Adresses  

adresses_df = san.get(
    "daily_active_addresses/santiment",
    from_date="2018-06-01",
    to_date="2018-06-05",
    interval="1d"
)

# Active Adresses with default parameters (last year with 1 d interval)

adresses_dp = san.get("daily_active_addresses/santiment")

# Prices

prices_df = san.get(
    "prices/santiment",
    from_date="2018-06-01",
    to_date="2018-06-05",
    interval="1d"
)

# Prices using default parameter

prices_dp = san.get("prices/santiment")

# Fetching metadata for an on-chain metric.

meta_data = san.metadata(
    "nvt",
    arr=['availableSlugs', 'defaultAggregation', 'humanReadableName', 'isAccessible', 'isRestricted', 'restrictedFrom', 'restrictedTo']
)


# See available metrics from slug

metrics_for_slug = san.available_metrics_for_slug('bitcoin')


# 

active_adresses_bitcoin = san.get(
    "active_addresses_24h/bitcoin",
    from_date="2018-06-01",
    to_date=datetime.datetime.now(),
    interval="1d"
)






