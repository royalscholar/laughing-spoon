from ib_insync import *
import pandas as pd
import numpy as np
import time
from strategies.macross import Strategy

# =========================
# CONFIG
# =========================
PORT = 7496          # Paper
CLIENT_ID = 1

QTY = 5
SLEEP_TIME = 60

MAX_OPEN_POSITIONS = 3
MAX_DOLLAR_PER_TRADE = 150
MAX_ACCOUNT_EXPOSURE = 0.25   # 25%

# =========================
# CONNECT
# =========================
ib = IB()
print("Connecting to IBKR...")
ib.connect("127.0.0.1", PORT, clientId=CLIENT_ID)
print("Connected:", ib.isConnected())

# =========================
# LOAD SYMBOLS
# =========================
tickers = pd.read_excel("Data/tickers_us_clean.xlsx")["symbol"].tolist()
tickers = tickers[:50]  # keep visible for demo

print(f"Loaded {len(tickers)} symbols")

strategy = Strategy()

# =========================
# HELPERS
# =========================
def contract(symbol):
    return Stock(symbol, "SMART", "USD")

def get_data(symbol):
    try:
        bars = ib.reqHistoricalData(
            contract(symbol),
            endDateTime="",
            durationStr="2 D",
            barSizeSetting="15 mins",
            whatToShow="TRADES",
            useRTH=True,
            formatDate=1
        )
        if not bars:
            return None
        df = util.df(bars)
        return df[["close"]]
    except:
        return None

def open_positions():
    return [p for p in ib.positions() if p.position != 0]

def account_value():
    for v in ib.accountValues():
        if v.tag == "NetLiquidation":
            return float(v.value)
    return 0

def exposure_used():
    exposure = 0
    for p in open_positions():
        exposure += abs(p.position * p.marketPrice)
    return exposure

# =========================
# RISK CHECK
# =========================
def risk_allowed(symbol, price):
    positions = open_positions()

    if len(positions) >= MAX_OPEN_POSITIONS:
        print("⛔ Risk: Max open positions reached")
        return False

    if price * QTY > MAX_DOLLAR_PER_TRADE:
        print(f"⛔ Risk: Trade too large for {symbol}")
        return False

    acct = account_value()
    if acct == 0:
        return False

    if exposure_used() / acct > MAX_ACCOUNT_EXPOSURE:
        print("⛔ Risk: Account exposure limit hit")
        return False

    return True

# =========================
# EXECUTION
# =========================
def place_trade(symbol, action, qty):
    try:
        c = contract(symbol)
        ib.qualifyContracts(c)
        order = MarketOrder(action, qty)
        trade = ib.placeOrder(c, order)
        ib.sleep(1)
        print(f"✅ ORDER: {action} {qty} {symbol} | {trade.orderStatus.status}")
    except Exception as e:
        print(f"Trade error {symbol}: {e}")

# =========================
# MAIN LOOP
# =========================
print("🚀 IBKR MA BOT WITH RISK MANAGEMENT STARTED")

while True:
    print("\n--- New Cycle ---")
    print("Open positions:", len(open_positions()))

    for symbol in tickers:
        df = get_data(symbol)
        if df is None or len(df) < 30:
            continue

        price = df["close"].iloc[-1]
        signal = strategy.generate_signal(df)

        pos = [p for p in open_positions() if p.contract.symbol == symbol]
        pos_qty = pos[0].position if pos else 0

        print(symbol, "Signal:", signal, "| Position:", pos_qty)

        if signal == "BUY" and pos_qty == 0:
            if risk_allowed(symbol, price):
                place_trade(symbol, "BUY", QTY)

        elif signal == "SELL" and pos_qty > 0:
            place_trade(symbol, "SELL", pos_qty)

    print("Sleeping...\n")
    ib.sleep(SLEEP_TIME)
