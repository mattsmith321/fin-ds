from fin_ds.data_source_factory import DataSourceFactory


from portfoliovisualizer import PortfolioVisualizerDataSource

# data_sources = ["PortfolioVisualizer"]

# data_sources = DataSourceFactory.data_sources
# data_sources = ["AlphaVantage", "EODHD", "NasdaqDataLink", "Tiingo", "YFinance"]
data_sources = ["Tiingo"]

tickers = ["VFINX"]
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

DataSourceFactory.register_data_source(PortfolioVisualizerDataSource)

print(DataSourceFactory.data_sources)

for data_source in data_sources:
    print(f"Fetching data from {data_source}...")
    ds = DataSourceFactory(data_source)
    for ticker in tickers:
        print(f" - For ticker {ticker}...")

        df = ds.get_ticker_data(ticker)
        print(f"    - get_ticker_data(ticker) found {len(df)} records.")

        df = ds.get_ticker_data(ticker, backfill=True)
        print(f"    - get_ticker_data(ticker, backfill=True) found {len(df)} records.")

        df = ds.get_ticker_data(ticker, interval="monthly")
        print(
            f"    - get_ticker_data(ticker, , interval='monthly') found {len(df)} records."
        )

        df = ds.get_ticker_data(ticker, interval="monthly", backfill=True)
        print(
            f"    - get_ticker_data(ticker, interval='monthly', backfill=True) found {len(df)} records."
        )
