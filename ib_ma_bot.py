from ib_insync import *
import pandas as pd
import importlib
import time

# ============================================================
# CONNECT TO IBKR TWS / PAPER
# ============================================================

print("Connecting to IBKR...")
ib = IB()
ib.connect("127.0.0.1", 7497, clientId=101)
print("Connected:", ib.isConnected())


# ============================================================
# LOAD MOVING AVERAGE STRATEGY (macross.py)
# ============================================================

def load_strategy():
    try:
        module = importlib.import_module("strategies.macross")
        StrategyClass = getattr(module, "Strategy")
        return StrategyClass()
    except Exception as e:
        print("ERROR loading strategy:", e)
        return None


strategy = load_strategy()
if strategy is None:
    raise Exception("Strategy failed to load. Please check strategies/macross.py")


# ============================================================
# SYMBOL LISTS
# ============================================================

US_STOCKS = [
    "AAPL","MSFT","AMZN","META","TSLA",
    "NVDA","GOOG","AMD","NFLX","INTC",
    "JPM","BAC","V","MA","XOM",
    "CVX","KO","PEP","WMT","DIS"
]

CRYPTO = ["BTCUSD", "ETHUSD", "SOLUSD", "LTCUSD", "BCHUSD"]

FUTURES = [
    ("ES", "202503"),   # S&P500 E-mini
    ("NQ", "202503"),   # NASDAQ E-mini
    ("CL", "202502")    # Crude Oil
]


# ============================================================
# CONTRACT CREATOR FOR ALL ASSET TYPES
# ============================================================

def create_contract(symbol):

    # ----- CRYPTO -----
    if symbol in CRYPTO:
        return Crypto(symbol.replace("USD",""), "PAXOS", "USD")

    # ----- STOCKS -----
    if symbol in US_STOCKS:
        return Stock(symbol, "SMART", "USD")

    # ----- FUTURES -----
    for fut, expiry in FUTURES:
        if symbol.startswith(fut):
            return Future(fut, expiry, "CME")

    raise Exception(f"Unknown symbol: {symbol}")


# ============================================================
# GET PRICE DATA UNIVERSALLY
# ============================================================

def get_price_data(contract):

    try:
        bars = ib.reqHistoricalData(
            contract,
            endDateTime="",
            durationStr="2 D",
            barSizeSetting="5 mins",
            whatToShow="MIDPOINT",
            useRTH=False,
            formatDate=1
        )

        if not bars:
            return None

        df = util.df(bars)[["close"]]
        return df

    except Exception as e:
        print(f"Error fetching price data for {contract.symbol}: {e}")
        return None


# ============================================================
# SUBMIT ORDER
# ============================================================

def submit_order(symbol, contract, side):
    ib.qualifyContracts(contract)
    order = MarketOrder(side, 1)
    trade = ib.placeOrder(contract, order)
    ib.sleep(2)

    print(f"ORDER: {side} {symbol} status={trade.orderStatus.status}")


# ============================================================
# RUN BOT ON ALL SYMBOLS
# ============================================================

previous_signals = {}

def run_bot():
    all_symbols = US_STOCKS + CRYPTO + [f"{f[0]}{f[1]}" for f in FUTURES]

    print("\n📌 Starting Multi-Asset Moving Average Bot")
    print("Tracking:", ", ".join(all_symbols))
    print("-----------------------------------------------------")

    while True:

        for symbol in all_symbols:

            # ----- Create correct contract -----
            contract = create_contract(symbol)

            # ----- Fetch historical data -----
            df = get_price_data(contract)
            if df is None:
                print(f"NO DATA for {symbol}")
                continue

            # ----- Apply Moving Average Strategy -----
            signal = strategy.generate_signal(df)

            # Initialize memory
            if symbol not in previous_signals:
                previous_signals[symbol] = "HOLD"

            print(f"{symbol} → Signal: {signal}")

            # ----- Submit trades only on signal change -----
            if signal == "BUY" and previous_signals[symbol] != "BUY":
                submit_order(symbol, contract, "BUY")

            elif signal == "SELL" and previous_signals[symbol] != "SELL":
                submit_order(symbol, contract, "SELL")

            previous_signals[symbol] = signal

            ib.sleep(1)

        print("\n--- Cycle complete. Waiting 30 seconds ---\n")
        ib.sleep(30)


# ============================================================
# START BOT
# ============================================================

run_bot()
