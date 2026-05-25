import backtrader as bt

class RSI14Strategy(bt.Strategy):
    params = dict(
        rsi_period=14,
        oversold=30
    )

    def __init__(self):
        self.rsi = bt.ind.RSI(period=self.p.rsi_period)

    def next(self):
        if not self.position:
            if self.rsi < self.p.oversold:
                self.buy()
        else:
            if self.rsi > 50:
                self.sell()
