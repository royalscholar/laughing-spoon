import backtrader as bt
import pandas as pd
from alpaca_connect import get_data

class AlpacaData(bt.feeds.PandasData):
    """Custom Alpaca Data Feed for Backtrader."""
    params = (
        ('datetime', None),
        ('open', 'open'),
        ('high', 'high'),
        ('low', 'low'),
        ('close', 'close'),
        ('volume', 'volume'),
        ('openinterest', None),
    )

def get_bt_data(symbol, start, end):
    df = get_data(symbol, start, end)

    # Convert to Backtrader format
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    return AlpacaData(dataname=df)
