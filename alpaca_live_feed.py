import backtrader as bt
from alpaca.data.live import StockDataStream
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca_keys import API_KEY, API_SECRET, BASE_URL
import pandas as pd

class AlpacaLiveData(bt.feeds.PandasData):
    pass
