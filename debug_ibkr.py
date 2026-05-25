from ib_insync import *

print("Connecting to IBKR TWS...")
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# ⬅️ VERY IMPORTANT: FORCE FREE DELAYED MARKET DATA
ib.reqMarketDataType(3)  # 1=live, 2=frozen, 3=delayed, 4=delayed-frozen

contract = Stock('AAPL', 'SMART', 'USD')

print("Requesting REAL-TIME (DELAYED) market data...")
data = ib.reqMktData(contract, '', False, False)

ib.sleep(2)

print("Bid:", data.bid)
print("Ask:", data.ask)
print("Last:", data.last)

ib.disconnect()
