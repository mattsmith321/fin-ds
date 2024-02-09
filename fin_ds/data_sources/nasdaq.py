import nasdaqdatalink
import pandas as pd

from .base_data_source import BaseDataSource


class NasdaqDataSource(BaseDataSource):
    """
    A data source class for fetching historical stock data from the Nasdaq Data Link API.

    This class inherits from the BaseDataSource class and implements the
    necessary methods for fetching data from the API.

    Attributes:
        COLUMN_MAPPINGS (dict): A dictionary mapping API column names to custom column names.
        COLUMN_ORDER (list): A list defining the order of columns in the resulting DataFrame.

    """

    # Set this to False if no api key is required
    # Technically an API key is required, but the nasdaqdatalink library handles this for us
    # using the NASDAQ_DATA_LINK_API_KEY environment variable.
    api_key_required = False

    # All of the columns are already in the correct format, so we don't need to map any of them.
    COLUMN_MAPPINGS = {}

    COLUMN_ORDER = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "adj_open",
        "adj_high",
        "adj_low",
        "adj_close",
        "adj_volume",
        "ticker",
        "dividend",
        "split",
    ]

    def __init__(self, name, api_key, force_refresh=False):
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
        super().__init__(name, force_refresh)

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
        # If you don't have a paid subscription to the NASDAQ Data Link API, you can use the following
        # line to fetch data from the WIKI dataset, which is free.
        # df = nasdaqdatalink.Dataset(f"WIKI/{ticker}").data().to_pandas()

        df = nasdaqdatalink.get_table(
            "QUOTEMEDIA/PRICES",
            ticker=[f"{ticker}"],
            paginate=True,
        )

        # All the other data sources return a DataFrame with a "date" column
        # so we haven't had to set this manually.
        df = df.set_index("date")

        return df
