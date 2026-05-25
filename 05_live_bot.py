from ib_insync import *
import pandas as pd

# ----------------------------
# 1. Connect to IBKR
# ----------------------------
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=10)  # Single connection for all assets
print("Connected to IBKR:", ib.isConnected())

# ----------------------------
# 2. Define instruments
# ----------------------------
instruments = [
    {'type': 'forex', 'symbol': 'EURUSD', 'size': 10000},
    {'type': 'stock', 'symbol': 'AAPL', 'size': 10},
    {'type': 'crypto', 'symbol': 'BTCUSD', 'size': 0.01}
]

# ----------------------------
# 3. Function to get historical candles
# ----------------------------
def get_candles(contract):
    try:
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
    except Exception as e:
        print(f"Error fetching candles for {contract.symbol}: {e}")
        return None

# ----------------------------
# 4. Simple Moving Average Strategy
# ----------------------------
def strategy(df):
    if df is None or df.empty:
        return "HOLD"
    df['SMA'] = df['close'].rolling(20).mean()
    last_close = df['close'].iloc[-1]
    last_sma = df['SMA'].iloc[-1]

    if last_close > last_sma:
        return "BUY"
    elif last_close < last_sma:
        return "SELL"
    return "HOLD"

# ----------------------------
# 5. Place Market Order (with GTC)
# ----------------------------
def execute(contract, signal, size):
    if signal in ["BUY", "SELL"]:
        try:
            order = MarketOrder(
                action=signal,
                totalQuantity=size,
                tif='GTC'  # Good Till Cancelled to avoid 10349 error
            )
            trade = ib.placeOrder(contract, order)
            print(f"Order executed: {signal} {contract.symbol} size={size}")
        except Exception as e:
            print(f"Failed to place order for {contract.symbol}: {e}")
    else:
        print(f"No trade for {contract.symbol} - signal: {signal}")

# ----------------------------
# 6. Main Loop
# ----------------------------
while True:
    for inst in instruments:
        try:
            # Create contract object
            if inst['type'] == 'forex':
                contract = Forex(inst['symbol'])
            elif inst['type'] == 'stock':
                contract = Stock(inst['symbol'], 'SMART', 'USD')
            elif inst['type'] == 'crypto':
                contract = Crypto(inst['symbol'])
            else:
                continue

            # Fetch candles
            df = get_candles(contract)

            # Generate signal
            signal = strategy(df)

            # Execute order
            execute(contract, signal, inst['size'])

            # Fetch live market data
            ticker = ib.reqMktData(contract)
            ib.sleep(1)
            print(f"{contract.symbol} Bid: {ticker.bid} Ask: {ticker.ask} Signal: {signal}")

        except Exception as e:
            print(f"Error processing {inst['symbol']}: {e}")

    # Wait 1 minute before next iteration
    ib.sleep(60)
