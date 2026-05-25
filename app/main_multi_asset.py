from ib_insync import *
import time

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=10)
print("Connected to IBKR:", ib.isConnected())

# Contracts
forex = Forex('EURUSD')
stock = Stock('AAPL', 'SMART', 'USD')
crypto = Crypto('BTCUSD', 'COINBASE')  # Use valid exchange

contracts = [forex, stock, crypto]

# Strategy logic placeholder
def get_signal(contract):
    try:
        ticker = ib.reqMktData(contract, snapshot=True)
        ib.sleep(2)
        bid, ask = ticker.bid, ticker.ask
        if bid is None or ask is None:
            return "HOLD"
        mid = (bid + ask)/2
        if mid % 2 > 1:
            return "BUY"
        else:
            return "SELL"
    except Exception as e:
        print(f"Market data error for {contract.symbol}: {e}")
        return "HOLD"

def execute_order(contract, signal, qty):
    if signal in ["BUY", "SELL"]:
        order = MarketOrder(signal, qty)
        order.tif = 'GTC'  # Fix for Forex 10349
        ib.placeOrder(contract, order)
        print(f"Order executed: {signal} {contract.symbol} qty={qty}")
    else:
        print(f"No trade for {contract.symbol} - signal: {signal}")

while True:
    for c in contracts:
        signal = get_signal(c)
        execute_order(c, signal, 1 if c.symbol != 'BTCUSD' else 0.01)
    ib.sleep(60)
