import pandas as pd
from alpha_vantage.timeseries import TimeSeries

from fin_ds.data_sources.base_data_source import BaseDataSource


class AlphaVantageDataSource(BaseDataSource):

    COLUMN_MAPPINGS = {
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. adjusted close": "adj_close",
        "6. volume": "volume",
        "7. dividend amount": "dividend",
    }

    COLUMN_ORDER = [
        "ticker",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "adj_close",
        "dividend",
    ]

    def __init__(self, name, api_key, force_refresh=False):
        # Call the base class __init__
        super().__init__(name, force_refresh)

        self.api_client = TimeSeries(key=api_key, output_format="pandas")

    def _fetch_data_from_source(self, ticker) -> pd.DataFrame:
        # The get_daily_adjusted method is a PRO feature and requires paying for the API.
        # For now, we'll use the get_monthly_adjusted method, which is free.
        df = self.api_client.get_monthly_adjusted(ticker)[0]

        return df
