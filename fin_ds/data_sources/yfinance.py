import pandas as pd

from fin_ds.data_source_factory import DataSourceFactory
from fin_ds.data_sources.base_data_source import BaseDataSource


class YFinanceDataSource(BaseDataSource):
    # Set this to False if no api key is required
    api_key_required = False

    COLUMN_MAPPINGS = {
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume",
    }

    COLUMN_ORDER = [
        "ticker",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "adj_close",
    ]

    def __init__(self, name, api_key):
        # Call the base class __init__
        super().__init__(name)

    def _fetch_data_from_source(self, ticker) -> pd.DataFrame:
        """
        Fetch historical stock data for a given ticker symbol within a date range.

        Args:
            ticker (str): The stock ticker symbol (e.g., "AAPL").

        Returns:
            list: A list of historical stock data points (e.g., OHLC prices) as dictionaries.
        """
        # Lazy load the library to avoid importing it if not needed
        import yfinance as api_client

        df = api_client.download(ticker, interval="1d", progress=False)

        return df


DataSourceFactory.register_data_source(YFinanceDataSource)
