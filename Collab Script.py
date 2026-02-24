import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import pandas_ta_classic as ta
import yfinance as yf
import requests
import matplotlib as plt
from math import sqrt
import platform
# Price Data
price_daily = pd.read_excel('ASX200_prices_3y_1d.xlsx')
price_daily = price_daily.set_index('Date')
price_daily = price_daily.dropna(axis = 1)
price_daily.head()
daily_returns = price_daily.pct_change()
daily_returns = daily_returns.dropna(axis = 0)

# Info
company_info = pd.read_excel('ASX200_company_info.xlsx')
ticker_industry = company_info
