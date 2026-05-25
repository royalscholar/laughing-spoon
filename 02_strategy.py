from ib_insync import *
import pandas as pd

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=2)

contract = Forex('EURUSD')

def get_candles():
    """Fetch last 100 candles."""
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting='5 mins',
        whatToShow='MIDPOINT',
        useRTH=False
    )
    df = util.df(bars)
    return df

def strategy(df):
    """Simple Moving Average strategy."""
    df['SMA'] = df['close'].rolling(20).mean()

    last_close = df['close'].iloc[-1]
    last_sma = df['SMA'].iloc[-1]

    if last_close > last_sma:
        return "BUY"
    elif last_close < last_sma:
        return "SELL"
    else:
        return "HOLD"

# Run strategy
df = get_candles()
signal = strategy(df)

print("Strategy signal:", signal)
