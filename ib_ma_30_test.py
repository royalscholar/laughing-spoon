from ib_insync import *
import pandas as pd
import time
from strategies.macross import Strategy

# =========================
# CONFIG — $30 LIVE TEST
# =========================
PORT = 7497          # 7497 = Paper, 7496 = Live
CLIENT_ID = 19

SYMBOL = "F"      # ~$20–25 stock
QTY = 1              # 1 share only
MAX_POSITION = 1     # Hard risk cap
SLEEP_TIME = 60      # 1 minute

# =========================
# CONNECT
# =========================
ib = IB()
print("🔌 Connecting to IBKR...")
ib.connect("127.0.0.1", PORT, clientId=CLIENT_ID, timeout=10)
print("✅ Connected:", ib.isConnected())

# =========================
# CONTRACT
# =========================
contract = Stock(SYMBOL, "SMART", "USD")
ib.qualifyContracts(contract)

# =========================
# STRATEGY
# =========================
strategy = Strategy()

# =========================
# HELPERS
# =========================
def get_position():
    for p in ib.positions():
        if p.contract.symbol == SYMBOL:
            return p.position
    return 0

def get_data():
    bars = ib.reqHistoricalData(
        contract,
        endDateTime="",
        durationStr="2 D",
        barSizeSetting="5 mins",
        whatToShow="TRADES",
        useRTH=True,
        formatDate=1
    )
    if not bars:
        return None
    df = util.df(bars)
    return df[["close"]]

def place_order(action):
    order = MarketOrder(action, QTY)
    trade = ib.placeOrder(contract, order)
    ib.sleep(2)
    print(f"📥 ORDER SENT: {action} {QTY} {SYMBOL} | Status: {trade.orderStatus.status}")

# =========================
# MAIN LOOP
# =========================
print(f"🚀 $30 LIVE TEST BOT STARTED FOR {SYMBOL}")

previous_signal = "HOLD"

while True:
    df = get_data()
    if df is None:
        print("⚠️ No data")
        ib.sleep(SLEEP_TIME)
        continue

    signal = strategy.generate_signal(df)
    position = get_position()

    print(f"{SYMBOL} | Signal: {signal} | Position: {position}")

    # BUY
    if signal == "BUY" and position == 0:
        place_order("BUY")

    # SELL
    elif signal == "SELL" and position > 0:
        place_order("SELL")

    ib.sleep(SLEEP_TIME)
