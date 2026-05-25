from ib_insync import *
import time
import pandas as pd
import csv

# -------------------------------
# 1. Connect to IBKR TWS
# -------------------------------
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=20)  # Paper account port
print("Connected to IBKR:", ib.isConnected())

# -------------------------------
# 2. Define Contracts
# -------------------------------
forex = Forex('EURUSD')
stock = Stock('AAPL', 'SMART', 'USD')
crypto = Crypto('BTCUSD', 'COINBASE')  # Change exchange if needed

contracts = [forex, stock, crypto]

# -------------------------------
# 3. Strategy Parameters
# -------------------------------
SMA_PERIOD = 20
RSI_PERIOD = 14

MAX_RISK_PER_TRADE = 0.02  # 2% of portfolio per trade
STOP_LOSS = 0.002          # Example: 0.2% for Forex
TAKE_PROFIT = 0.004        # Example: 0.4% for Forex

# -------------------------------
# 4. Utility Functions
# -------------------------------
def get_price(contract):
    try:
        ticker = ib.reqMktData(contract, snapshot=True)
        ib.sleep(2)
        bid, ask = ticker.bid, ticker.ask
        if bid is None or ask is None:
            print(f"Price not available for {contract.symbol}")
            return None
        return (bid + ask) / 2
    except Exception as e:
        print(f"Market data error for {contract.symbol}: {e}")
        return None

def calculate_sma(prices, period=SMA_PERIOD):
    return pd.Series(prices).rolling(period).mean().iloc[-1]

def calculate_rsi(prices, period=RSI_PERIOD):
    delta = pd.Series(prices).diff()
    gain = delta.where(delta>0,0)
    loss = -delta.where(delta<0,0)
    avg_gain = gain.rolling(period).mean().iloc[-1]
    avg_loss = loss.rolling(period).mean().iloc[-1]
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100/(1+rs))

# -------------------------------
# 5. Strategy Logic
# -------------------------------
def get_signal(contract, history_prices):
    if len(history_prices) < SMA_PERIOD + 1:
        return "HOLD"
    sma = calculate_sma(history_prices)
    rsi = calculate_rsi(history_prices)
    last_price = history_prices[-1]

    if last_price > sma and rsi < 70:
        return "BUY"
    elif last_price < sma and rsi > 30:
        return "SELL"
    return "HOLD"

# -------------------------------
# 6. Position Sizing
# -------------------------------
def get_qty(contract, price):
    if price is None or pd.isna(price):
        print(f"Skipping {contract.symbol} - price not available")
        return 0

    account_summary = ib.accountSummary()  # returns list of AccountSummaryTag
    cash = 0
    for tag in account_summary:
        if tag.tag == 'NetLiquidation':
            cash = float(tag.value)
            break
    if cash == 0:
        print("Warning: Could not fetch NetLiquidation, defaulting qty=1")
        return 1

    qty = cash * MAX_RISK_PER_TRADE / price
    if contract.symbol == 'BTCUSD':
        return round(qty, 4)
    else:
        return max(1, int(qty))

# -------------------------------
# 7. Execute Orders with Bracket (SL/TP)
# -------------------------------
def execute_order(contract, signal, price):
    qty = get_qty(contract, price)
    if qty == 0:
        print(f"Skipping {contract.symbol} - qty=0")
        return

    if signal in ["BUY", "SELL"]:
        # Create bracket order
        if signal == "BUY":
            stop_loss_price = price * (1 - STOP_LOSS)
            take_profit_price = price * (1 + TAKE_PROFIT)
        else:
            stop_loss_price = price * (1 + STOP_LOSS)
            take_profit_price = price * (1 - TAKE_PROFIT)

        bracket = ib.bracketOrder(signal, qty, take_profit_price, stop_loss_price, tif='GTC')
        for o in bracket:
            ib.placeOrder(contract, o)

        print(f"Bracket order executed: {signal} {contract.symbol} qty={qty} | SL: {stop_loss_price:.5f} TP: {take_profit_price:.5f}")

        # Log trade
        with open('trade_log.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([contract.symbol, signal, qty, price, stop_loss_price, take_profit_price, time.time()])
    else:
        print(f"No trade for {contract.symbol} - signal: {signal}")

# -------------------------------
# 8. Main Loop
# -------------------------------
history = {c.symbol: [] for c in contracts}  # store historical prices

while True:
    for c in contracts:
        price = get_price(c)
        if price is None:
            continue
        # Update price history
        history[c.symbol].append(price)
        if len(history[c.symbol]) > 100:
            history[c.symbol].pop(0)
        # Get trade signal
        signal = get_signal(c, history[c.symbol])
        # Execute trade
        execute_order(c, signal, price)
    ib.sleep(60)  # repeat every 1 minute
