from ib_insync import *

# 1. Create IB object
ib = IB()

# 2. Connect to TWS (paper trading port 7497)
ib.connect('127.0.0.1', 7497, clientId=1)

print("Connected to IBKR:", ib.isConnected())

# 3. Define contract (EURUSD forex)
contract = Forex('EURUSD')

# 4. Request market data
ticker = ib.reqMktData(contract)

# 5. Print live data continuously
while True:
    ib.sleep(1)
    print("Bid:", ticker.bid, "Ask:", ticker.ask)
