import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import pandas_ta_classic as ta
import yfinance as yf
import requests
import matplotlib.pyplot as plt
from math import sqrt
import platform
def data_cleaner(df):
    df = df.set_index('Date')
    df = df.dropna()
    return df

# 'price_daily = pd.read_excel('ASX200_prices_3y_1d.xlsx') 
# price_daily = price_daily.set_index('Date')
# price_daily = price_daily.dropna(axis = 1)
# daily_returns = price_daily.pct_change()
# daily_returns = daily_returns.dropna(axis = 0)'


## Sector Dataset
from pandas import to_datetime


company_info = pd.read_excel('ASX200_company_info.xlsx')
ticker_sector = company_info[['Ticker', 'Sector']]
Sector_prices = pd.read_csv('Sector Indices.csv').drop('Market', axis = 1)
Sector_prices = Sector_prices.set_index('Date')
Sector_prices.index = to_datetime(Sector_prices.index)
Sector_prices = Sector_prices.resample('ME').last()
sector_delta = Sector_prices.pct_change()
sector_delta = sector_delta.dropna(axis = 0)


sector_change5y = sector_delta.loc['2021-01-31':'2026-01-31']
# Yield Dataset
from pandas import to_datetime
import warnings
warnings.filterwarnings('ignore')

yields_df = pd.read_csv('10YRTreasury.csv')
yields_df = data_cleaner(yields_df)
yields_df.index = to_datetime(yields_df.index)
yields_df = yields_df.resample('ME').last()
yield_change = yields_df.pct_change().dropna()


ten_two_yield = yields_df[['Australian Government 2 year bond','Australian Government 10 year bond']]
ten_two_yield['Slope'] = ten_two_yield['Australian Government 10 year bond'] - ten_two_yield['Australian Government 2 year bond']
ten_two_yield_5y = ten_two_yield.loc['2021-01-31':]
yield_bps_change_5y = ten_two_yield.diff().loc['2021-01-31':]
yield_bps_change_5y = yield_bps_change_5y.rename(columns={
    'Australian Government 2 year bond': 'AU 2Y Yield Change',
    'Australian Government 10 year bond': 'AU 10Y Yield Change',
    'Slope': 'AU 10Y-2Y Slope Change'
})
yield_bps_change_5y
plt.style.use('default')
plt.autoscale(enable=True, axis='x')
plt.plot(yield_bps_change_5y.index, ten_two_yield_5y['Slope'])
plt.xlabel('Date')
plt.ylabel('Yield Slope')
plt.title('Yield Slope Curve')
plt.gcf().autofmt_xdate()
plt.show()
## Sector Momentum Marker/Ranker 
# Helper Functions
N = len(Sector_prices.columns)
def ranker(df):
    ranked_df = df.copy()
    # Keep rows, edit every column
    ranked_df = ranked_df.rank(ascending = False, axis = 0)
    return ranked_df

def scorer(df):
    return 1 -(df - 0.5)/(N)
