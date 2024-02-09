from fin_ds.data_source_factory import DataSourceFactory


data_sources = DataSourceFactory.DATA_SOURCES
# data_sources = ["Nasdaq"]
tickers = ["AAPL"]

for data_source in data_sources:
    ds = DataSourceFactory(data_source)
    print(f"Fetching data from {data_source}...")
    for ticker in tickers:
        print(f" - For ticker {ticker}...")

        df = ds.get_ticker_data(ticker)
        print(f"    - get_ticker_data(ticker) found {len(df)} records.")

        df = ds.get_ticker_data(ticker, "monthly")
        print(f"    - get_ticker_data(ticker, 'monthly') found {len(df)} records.")
