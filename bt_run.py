# ==============================
# bt_run.py  (FINAL CLEAN VERSION)
# ==============================

import argparse
import backtrader as bt
import pandas as pd

from alpaca_connect import get_data
from Strategies.MaCrossStrategy import MaCrossStrategy
from Strategies.RsiStrategy import RsiStrategy
from Strategies.BreakoutStrategy import BreakoutStrategy


def run_backtest(symbol, start, end, strategy_name):
    df = get_data(symbol, start, end)  # OHLCV dataframe

    # Convert dataframe → Backtrader feed
    data = bt.feeds.PandasData(
        dataname=df,
        datetime=None,
        open="open",
        high="high",
        low="low",
        close="close",
        volume="volume",
    )

    cerebro = bt.Cerebro()

    if strategy_name == "macross":
        cerebro.addstrategy(MaCrossStrategy)
    elif strategy_name == "rsi":
        cerebro.addstrategy(RsiStrategy)
    elif strategy_name == "breakout":
        cerebro.addstrategy(BreakoutStrategy)
    else:
        raise ValueError("Unknown strategy!")

    cerebro.adddata(data)
    cerebro.run()
    cerebro.plot()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str)
    parser.add_argument("--start", type=str)
    parser.add_argument("--end", type=str)
    parser.add_argument("--strategy", type=str)
    args = parser.parse_args()

    run_backtest(args.symbol, args.start, args.end, args.strategy)
