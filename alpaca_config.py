# alpaca_config.py

from alpaca_connect import get_data

print("Fetching data from Alpaca...")

df = get_data("AAPL", start="2022-01-01", end="2022-05-01")

print(df.head())
print("Data fetch successful!")
