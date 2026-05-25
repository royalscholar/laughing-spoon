import backtrader as bt
import yfinance as yf
import pandas as pd

# ---------------------------
# 1. Define Strategy
# ---------------------------
class SMACrossStrategy(bt.Strategy):
    params = dict(fast=20, slow=50)

    def __init__(self):
        sma_fast = bt.indicators.SMA(self.data.close, period=self.p.fast)
        sma_slow = bt.indicators.SMA(self.data.close, period=self.p.slow)
        self.crossover = bt.indicators.CrossOver(sma_fast, sma_slow)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
            elif self.crossover < 0:
                self.sell()
        else:
            if self.position.size > 0 and self.crossover < 0:
                self.close()
                self.sell()
            elif self.position.size < 0 and self.crossover > 0:
                self.close()
                self.buy()

# ---------------------------
# 2. Define a function to download and clean data
# ---------------------------
def get_data(symbol, start, end, interval='1d'):
    data = yf.download(symbol, start=start, end=end, interval=interval)
    data = data[['Open','High','Low','Close','Volume']]
    data.columns = ['open','high','low','close','volume']
    data['openinterest'] = 0
    data.dropna(inplace=True)
    return bt.feeds.PandasData(dataname=data)

# ---------------------------
# 3. Setup Cerebro
# ---------------------------
cerebro = bt.Cerebro()
cerebro.broker.set_cash(10000)

# Add analyzers
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

# ---------------------------
# 4. Add assets
# ---------------------------
assets = ['EURUSD=X', 'AAPL', 'BTC-USD']  # Forex, Stock, Crypto
for symbol in assets:
    datafeed = get_data(symbol, start="2018-01-01", end="2025-01-01")
    cerebro.adddata(datafeed, name=symbol)

# ---------------------------
# 5. Add strategy
# ---------------------------
cerebro.addstrategy(SMACrossStrategy)

# ---------------------------
# 6. Run backtest
# ---------------------------
results = cerebro.run()
strat = results[0]

# ---------------------------
# 7. Print performance metrics
# ---------------------------
print("===== PERFORMANCE METRICS =====")
print("Final Portfolio Value:", cerebro.broker.getvalue())
print("Sharpe Ratio:", strat.analyzers.sharpe.get_analysis())
print("Max Drawdown (%):", strat.analyzers.drawdown.get_analysis().max.drawdown)
print("Total Return (%):", strat.analyzers.returns.get_analysis().get('rtot'))
print("Annual Return (%):", strat.analyzers.returns.get_analysis().get('rnorm'))
