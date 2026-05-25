# Strategies/rsi.py
import backtrader as bt

class RsiStrategy(bt.Strategy):
    params = dict(period=14, overbought=70, oversold=30)

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.p.period)

    def next(self):
        if not self.position:
            if self.rsi < self.p.oversold:
                self.buy()
        else:
            if self.rsi > self.p.overbought:
                self.close()
