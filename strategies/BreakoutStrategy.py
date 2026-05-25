# Strategies/breakout.py
import backtrader as bt

class BreakoutStrategy(bt.Strategy):
    params = dict(period=20)

    def __init__(self):
        self.high = bt.indicators.Highest(self.data.high, period=self.p.period)
        self.low = bt.indicators.Lowest(self.data.low, period=self.p.period)

    def next(self):
        if not self.position:
            if self.data.close[0] > self.high[-1]:
                self.buy()
        else:
            if self.data.close[0] < self.low[-1]:
                self.close()
