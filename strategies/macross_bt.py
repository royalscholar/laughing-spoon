# Strategies/macross.py
import backtrader as bt

class MaCrossStrategy(bt.Strategy):
    params = dict(fast=20, slow=50)

    def __init__(self):
        self.sma_fast = bt.indicators.SimpleMovingAverage(self.data.close, period=self.p.fast)
        self.sma_slow = bt.indicators.SimpleMovingAverage(self.data.close, period=self.p.slow)
        self.cross = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)

    def next(self):
        if not self.position:
            if self.cross > 0:
                self.buy()
        else:
            if self.cross < 0:
                self.close()
