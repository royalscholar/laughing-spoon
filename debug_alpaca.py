from alpaca_connect import get_data

df = get_data("AAPL", "2022-01-01", "2022-05-01")

print("\n=== COLUMNS ===")
print(df.columns)

print("\n=== HEAD ===")
print(df.head())

print("\n=== INDEX ===")
print(df.index)
