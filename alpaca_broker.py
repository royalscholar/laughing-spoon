import backtrader as bt
from alpaca.broker import Broker
from alpaca.trading.client import TradingClient
from alpaca_keys import API_KEY, API_SECRET, BASE_URL

def get_alpaca_broker():
    trading_client = TradingClient(API_KEY, API_SECRET, paper=True)

    broker = Broker(
        client=trading_client,
        data_feed=None,  
    )
    return broker
