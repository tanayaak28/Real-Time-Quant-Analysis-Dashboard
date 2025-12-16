import pandas as pd

class TickStore:
    def __init__(self):
        self.df = pd.DataFrame(columns=["ts", "symbol", "price", "qty"])

    def update(self, ticks):
        if ticks:
            self.df = pd.concat([self.df, pd.DataFrame(ticks)])
            self.df.drop_duplicates(inplace=True)

    def resample(self, symbol, timeframe):
        sdf = self.df[self.df["symbol"] == symbol]
        if sdf.empty:
            return sdf
        sdf = sdf.set_index("ts")
        rule = {"1s": "1S", "1m": "1T", "5m": "5T"}[timeframe]
        return sdf.resample(rule).agg({"price": "last", "qty": "sum"}).dropna()
