import logging
from abc import ABC

import pandas as pd

from fin_ds.utils.cache_util import CacheUtil
from fin_ds.utils.df_util import DFUtil

logger = logging.getLogger(__name__)


class BaseDataSource(ABC):
    # If a data source requires an API key, this should be set to True.
    # But if the data source does not require an API key, this should
    # be set to False in the subclass.
    api_key_required = True

    start_date = "1950-01-01"
    end_date = pd.Timestamp.today().strftime("%Y-%m-%d")

    def __init__(self, name):
        """
        Initialize the data source with a specific name.

        Args:
            name (str): The name of the data source.
        """
        self.name = name

    def get_eod_data(
        self,
        ticker: str,
        interval: str = "daily",
        backfill_ticker: str = None,
        max_cache_age_in_hours: int = 12,
    ) -> pd.DataFrame:
        """
        Fetch and return the data for a given ticker and aggregate it based on the specified interval.

        Args:
            ticker (str): The stock ticker symbol for which to fetch the data.
            interval (str, optional): The interval for data aggregation. Defaults to 'daily'.
                                    Supported values: 'daily', 'weekly', 'monthly'.
            backfill_ticker (str, optional): The ticker symbol to use for backfilling data. Defaults to None.
            max_cache_age_in_hours (int, optional): The maximum age of cached data. Defaults to 12.

        Returns:
            DataFrame: A pandas DataFrame containing the aggregated data.
        """
        original_df = self._fetch_data(ticker, max_cache_age_in_hours)

        combined_df = self._backfill_data(backfill_ticker, max_cache_age_in_hours, original_df)

        # Ensure the index is a DatetimeIndex especially after loading from cache
        combined_df.index = pd.to_datetime(combined_df.index)

        # Resample data based on the specified interval
        aggregated_df = self._aggregate_data(combined_df, interval)

        return aggregated_df

    def _backfill_data(self, backfill_ticker, max_cache_age_in_hours, original_df):
        """
        Backfill the original DataFrame with historical data from a specified backfill ticker.

        This method enhances the original dataset by incorporating additional historical data
        from the backfill ticker provided. If no backfill ticker is specified, it returns the
        original data unchanged.

        Args:
            backfill_ticker (str): The ticker symbol to use for backfilling data. If None or empty,
                                no backfilling is performed.
            max_cache_age_in_hours (int): The maximum age of cached data in hours. Used to determine
                                        whether to fetch fresh data.
            original_df (pd.DataFrame): The original DataFrame containing data for the primary ticker.

        Returns:
            pd.DataFrame: A DataFrame that combines the original data with backfilled data if a
                        backfill ticker is provided; otherwise, returns the original data.
        """
        if backfill_ticker:
            # Fetch data for the backfill ticker, respecting the maximum cache age
            backfill_df = self._fetch_data(backfill_ticker, max_cache_age_in_hours)
            # Combine the original DataFrame with the backfill DataFrame
            # DFUtil.splice is assumed to merge dataframes by aligning on the index and filling gaps
            return DFUtil.splice(original_df, backfill_df)
        else:
            # No backfill ticker provided; return the original DataFrame unmodified
            return original_df

    def _fetch_data(self, ticker: str, max_cache_age_in_hours: int) -> pd.DataFrame:
        """
        Retrieve data for the given ticker symbol. This method first checks if
        the data is available in the cache. If it is, the cached data is returned.
        Otherwise, it fetches the data from the data source by calling the
        subclass-specific _fetch_data_from_source method, caches it, and then returns it.

        This method is intended to be used internally within the class and its
        subclasses, and it abstracts away the caching logic to avoid repetition
        in each data source subclass.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the data for the specified ticker.
                          The data is either retrieved from the cache or directly from
                          the data source.
        """
        cache_path = CacheUtil.cache_path(self.name, ticker)

        # Check if data is cached and not stale
        if CacheUtil.is_cached(cache_path):
            if not CacheUtil.is_stale(cache_path, max_cache_age_in_hours):
                logger.info(f"Loading data for {ticker} from cache.")
                cached_df = CacheUtil.load_from_cache(cache_path)
                return cached_df
            else:
                logger.info(f"Cache for {ticker} is stale.")
        else:
            logger.info(f"No cache found for {ticker}.")

        # Fetch and cache data
        try:
            logger.info(f"Fetching data for {ticker}...")
            latest_df = self._fetch_and_process_data(ticker)
        except Exception as e:
            logger.error(f"Failed to fetch data for {ticker}: {e}")
            raise

        CacheUtil.save_to_cache(cache_path, latest_df)
        logger.info(f"Data for {ticker} fetched and cached.")

        return latest_df

    def _fetch_and_process_data(self, ticker: str) -> pd.DataFrame:
        # Fetch data from source via subclass-specific method
        source_df = self._fetch_data_from_source(ticker)

        # Standardize the DataFrame
        processed_df = self._preprocess_data(ticker, source_df)

        return processed_df

    def _preprocess_data(self, ticker: str, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize the DataFrame by renaming columns and reordering them.

        Args:
            df (pd.DataFrame): The DataFrame to standardize.

        Returns:
            pd.DataFrame: The standardized DataFrame.
        """
        # Rename columns
        df = df.rename(columns=self.COLUMN_MAPPINGS)

        # Add the ticker as a column. Used when backfilled data is added.
        if "ticker" not in df.columns:
            df["ticker"] = ticker

        # Reorder columns
        df = df[self.COLUMN_ORDER]

        # Change the index name
        df.index.name = "date"

        # Remove any time-related data from the index so that we end up with yyyy-mm-dd
        df.index = pd.to_datetime(df.index).tz_localize(None)

        # Sort by date in ascending order
        df = df.sort_values(by="date")

        # Round only the floating-point columns in latest_df.
        # Without this, Yahoo Finance was flagging tons of records with differences.
        # Multiple requests for the same data would return slightly different values
        # way down in the precision. With this, updates tend to be consistent and
        # mainly focus on the adjusted close column.
        # numeric_cols = df.select_dtypes(include=["float64"]).columns
        # df[numeric_cols] = df[numeric_cols].round(12)

        return df

    def _aggregate_data(self, df: pd.DataFrame, interval: str) -> pd.DataFrame:
        """Aggregate data based on the specified interval."""
        resample_rules = {
            "daily": None,
            "weekly": "W",
            "monthly": "ME",
        }

        freq = resample_rules.get(interval)
        if freq is None and interval != "daily":
            raise ValueError(
                f"Unsupported interval: {interval}. Supported intervals are 'daily', 'weekly', 'monthly'."
            )

        if freq:
            return df.resample(freq).last()
        else:
            return df
