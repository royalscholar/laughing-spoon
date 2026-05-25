from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=4)

contract = Forex('EURUSD')

def check_positions():
    positions = ib.positions()
    for pos in positions:
        print(pos)

def close_all_positions():
    order = MarketOrder("SELL", 10000)  # reverse
    ib.placeOrder(contract, order)
    print("Closed all positions")

check_positions()
