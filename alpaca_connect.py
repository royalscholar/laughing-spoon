# ======================================
# alpaca_connect.py  (FINAL CLEAN VERSION)
# ======================================

import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca_keys import API_KEY, API_SECRET

client = StockHistoricalDataClient(API_KEY, API_SECRET)


def get_data(symbol, start, end):
    print("📡 Fetching data from Alpaca...")

    request = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame.Day,
        start=start,
        end=end
    )

    raw = client.get_stock_bars(request)
    bars = raw.df  # Alpaca returns MULTI-INDEX dataframe

    # --------------------------------------
    # FIX MULTI-INDEX (timestamp, symbol)
    # --------------------------------------
    if isinstance(bars.index, pd.MultiIndex):
        bars = bars.reset_index()  # remove multi index

    # --------------------------------------
    # KEEP ONLY THIS SYMBOL
    # --------------------------------------
    if "symbol" in bars.columns:
        bars = bars[bars["symbol"] == symbol]

    # --------------------------------------
    # Set index to timestamp column
    # --------------------------------------
    time_col = None
    for col in bars.columns:
        if "timestamp" in col.lower():
            time_col = col
            break

    if time_col is None:
        raise ValueError("❌ No timestamp column found in Alpaca Data!")

    bars[time_col] = pd.to_datetime(bars[time_col])
    bars = bars.set_index(time_col)

    # --------------------------------------
    # Rename Alpaca columns → Backtrader format
    # --------------------------------------
    rename_map = {
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
    }
    bars = bars.rename(columns=rename_map)

    # Keep only needed columns
    bars = bars[["open", "high", "low", "close", "volume"]]

    print("✅ Data fetched successfully!")
    return bars
