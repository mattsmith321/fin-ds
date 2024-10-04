import pandas as pd

from fin_ds.data_source_factory import DataSourceFactory
from fin_ds.data_sources.base_data_source import BaseDataSource


class TiingoDataSource(BaseDataSource):
    """
    A data source class for fetching historical stock data from the Tiingo API.

    This class inherits from the BaseDataSource class and implements the necessary methods
    for fetching data from the Tiingo API.

    Attributes:
        COLUMN_MAPPINGS (dict): A dictionary mapping Tiingo API column names to custom column names.
        COLUMN_ORDER (list): A list defining the order of columns in the resulting DataFrame.

    """

    COLUMN_MAPPINGS = {
        "adjClose": "adj_close",
        "adjHigh": "adj_high",
        "adjLow": "adj_low",
        "adjOpen": "adj_open",
        "adjVolume": "adj_volume",
        "divCash": "dividend",
        "splitFactor": "split",
    }

    COLUMN_ORDER = [
        "ticker",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "adj_open",
        "adj_high",
        "adj_low",
        "adj_close",
        "dividend",
        "split",
    ]

    def __init__(self, name, api_key):
        """
        Initialize a Tiingo data source object.

        Args:
            name (str): The name of the data source.
            api_key (str): The API key for accessing Tiingo data.
            force_refresh (bool, optional): Flag indicating whether to force data refresh. Defaults to False.

        Returns:
            None
        """
        # Call the base class __init__
        super().__init__(name)

        # Lazy load the library to avoid importing it if not needed
        from tiingo import TiingoClient

        tiingo_config = {"session": True, "api_key": api_key}
        self.api_client = TiingoClient(tiingo_config)

    def _fetch_data_from_source(self, ticker: str) -> pd.DataFrame:
        """
        Fetch historical stock data for a given ticker symbol from the Tiingo API.

        This method currently uses a hardcoded date range from 1950-01-01 to 2024-12-31.
        The frequency of the data is set to daily.

        Args:
            ticker (str): The stock ticker symbol (e.g., "AAPL").

        Returns:
            pd.DataFrame: A DataFrame containing the historical stock data. Each row represents a day,
            and the columns represent different data points such as open, high, low, close prices.
        """
        df = self.api_client.get_dataframe(
            ticker,
            fmt="json",
            startDate=self.start_date,
            endDate=self.end_date,
            frequency="daily",
        )

        return df


DataSourceFactory.register_data_source(TiingoDataSource)
