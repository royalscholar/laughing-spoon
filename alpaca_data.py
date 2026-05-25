from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import datetime

API_KEY = "PKLCDLG5B5PBXVWRRBMFCYYIEA"
API_SECRET = "3ZJFrTEYUjd8xkjtjcuGVQm2aWnJJndb9JoUWZqDuX5i"

client = StockHistoricalDataClient(API_KEY, API_SECRET)

def get_price(symbol):
    # Use yesterday's market session (this ALWAYS returns data)
    end = datetime.datetime.utcnow().date()
    start = end - datetime.timedelta(days=2)

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        start=start,
        end=end,
        feed="iex"
    )

    bars = client.get_stock_bars(request)

    # FIX: Alpaca returns list under bars.data
    bar_list = bars.data.get(symbol)

    if not bar_list:
        print("No data returned for this time window.")
        return None

    latest = bar_list[-1]

    print(f"Symbol: {symbol}")
    print("Latest Price:", latest.close)
    return latest.close


if __name__ == "__main__":
    get_price("AAPL")
