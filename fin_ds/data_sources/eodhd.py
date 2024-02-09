import pandas as pd
from eodhd import APIClient

from .base_data_source import BaseDataSource


class EODHDDataSource(BaseDataSource):
    COLUMN_MAPPINGS = {
        "adjusted_close": "adj_close",
    }

    COLUMN_ORDER = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "adj_close",
        "symbol",
        "interval",
    ]

    def __init__(self, name, api_key, force_refresh=False):
        # Call the base class __init__
        super().__init__(name, force_refresh)

        self.api_client = APIClient(api_key)

    def _fetch_data_from_source(self, ticker) -> pd.DataFrame:
        """
        Fetch historical stock data for a given ticker symbol within a date range.

        Args:
            ticker (str): The stock ticker symbol (e.g., "AAPL").

        Returns:
            list: A list of historical stock data points (e.g., OHLC prices) as dictionaries.
        """
        df = self.api_client.get_historical_data(
            ticker,
            "d",
            self.start_date,
            self.end_date,
        )

        return df
