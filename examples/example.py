from fin_ds.data_source_factory import DataSourceFactory


data_sources = DataSourceFactory.data_sources
# data_sources = ["Alpha Vantage", "EODHD", "Nasdaq", "Tiingo", "Yahoo Finance"]
# data_sources = ["Tiingo"]

tickers = ["AAPL"]
# tickers = [
#     "WMT",
#     "JNJ",
#     "PG",
#     "XOM",
#     "PFE",
#     "MSFT",
#     "KO",
#     "GE",
#     "BRK-A",
#     "IBM",
#     "VZ",
#     "INTC",
#     "CVX",
#     "JPM",
#     "BAC",
#     "GOOGL",
#     "AIG",
#     "WFC",
#     "AAPL",
#     "MRK",
# ]

print(DataSourceFactory.data_sources)

for data_source in data_sources:
    print(f"Fetching data from {data_source}...")
    ds = DataSourceFactory(data_source)
    for ticker in tickers:
        print(f" - For ticker {ticker}...")

        df = ds.get_ticker_data(ticker)
        print(f"    - get_ticker_data(ticker) found {len(df)} records.")

        df = ds.get_ticker_data(ticker, "monthly")
        print(f"    - get_ticker_data(ticker, 'monthly') found {len(df)} records.")
