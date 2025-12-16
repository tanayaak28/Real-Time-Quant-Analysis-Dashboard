import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

def hedge_ratio(x, y):
    return np.polyfit(x, y, 1)[0]

def spread_and_zscore(x, y, window=30):
    beta = hedge_ratio(x, y)
    spread = y - beta * x
    z = (spread - spread.rolling(window).mean()) / spread.rolling(window).std()
    return beta, spread, z

def rolling_correlation(x, y, window=30):
    return x.rolling(window).corr(y)

def adf_test(series):
    result = adfuller(series.dropna())
    return {
        "ADF Statistic": result[0],
        "p-value": result[1],
        "Critical Values": result[4]
    }
