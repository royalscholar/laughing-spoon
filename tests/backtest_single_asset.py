import backtrader as bt
import yfinance as yf
import pandas as pd

# ---------------------------
# 1. Download Data
# ---------------------------
data = yf.download("EURUSD=X", start="2018-01-01", end="2025-01-01", interval="1d")

# Fix column format for Backtrader
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
data.columns = ['open', 'high', 'low', 'close', 'volume']
data['openinterest'] = 0  # Required column

# Remove missing values
data.dropna(inplace=True)

# ---------------------------
# 2. Strategy
# ---------------------------
class SimpleStrategy(bt.Strategy):
    params = dict(period=14)

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.p.period)

    def next(self):
        if self.rsi < 30:        # Oversold → BUY
            self.buy()
        elif self.rsi > 70:      # Overbought → SELL
            self.sell()


# ---------------------------
# 3. Run Backtest
# ---------------------------
cerebro = bt.Cerebro()
cerebro.addstrategy(SimpleStrategy)

bt_data = bt.feeds.PandasData(dataname=data)
cerebro.adddata(bt_data)

cerebro.broker.set_cash(10000)

# Add analyzers
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

results = cerebro.run()
stats = results[0]

# ---------------------------
# 4. Print Results
# ---------------------------
print("===== PERFORMANCE METRICS =====")
print("Final Portfolio Value:", cerebro.broker.getvalue())

print("Sharpe Ratio:", stats.analyzers.sharpe.get_analysis())
print("Max Drawdown (%):", stats.analyzers.drawdown.get_analysis().max.drawdown)
print("Total Return (%):", stats.analyzers.returns.get_analysis().get('rtot'))
print("Annual Return (%):", stats.analyzers.returns.get_analysis().get('rnorm'))
