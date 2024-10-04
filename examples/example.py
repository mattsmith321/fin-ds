import logging
from fin_ds.data_source_factory import DataSourceFactory
from portfoliovisualizer import PortfolioVisualizerDataSource

# Configure the basic logging settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# data_sources = ["PortfolioVisualizer"]

# data_sources = DataSourceFactory.data_sources
# data_sources = ["AlphaVantage", "EODHD", "NasdaqDataLink", "Tiingo", "YFinance"]
data_sources = ["YFinance"]

tickers = ["^IRX"]
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

print(DataSourceFactory.get_data_source_names())

DataSourceFactory.register_data_source(PortfolioVisualizerDataSource)

print(DataSourceFactory.get_data_source_names())

for data_source in data_sources:
    print(f"Fetching data from {data_source}...")
    ds = DataSourceFactory(data_source)
    for ticker in tickers:
        print(f" - For ticker {ticker}...")

        df = ds.get_eod_data(ticker)
        print(f"    - get_eod_data(ticker) found {len(df)} records.")

        df = ds.get_eod_data(ticker, backfill_ticker="VUSTX")
        print(f"    - get_eod_data(ticker, backfill=True) found {len(df)} records.")

        df = ds.get_eod_data(ticker, interval="monthly")
        print(f"    - get_eod_data(ticker, , interval='monthly') found {len(df)} records.")

        df = ds.get_eod_data(ticker, interval="monthly", backfill_ticker="VUSTX")
        print(
            f"    - get_eod_data(ticker, interval='monthly', backfill_ticker=VUSTX) found {len(df)} records."
        )
