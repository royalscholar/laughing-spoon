from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=3)

contract = Forex('EURUSD')

def place_order(signal):

    if signal == "BUY":
        order = MarketOrder("BUY", 10000)  # 10k units
    elif signal == "SELL":
        order = MarketOrder("SELL", 10000)
    else:
        print("No trade executed")
        return

    trade = ib.placeOrder(contract, order)
    ib.sleep(1)
    print("Order placed:", signal)

# Example test
place_order("BUY")
