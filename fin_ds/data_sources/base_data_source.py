import logging
from abc import ABC

import pandas as pd

from fin_ds.backfill.backfill import Backfill
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

    def __init__(self, name, force_refresh=False):
        """
        Initialize the data source with a specific name.

        Args:
            name (str): The name of the data source.
        """
        self.name = name
        self.force_refresh = force_refresh

    def get_ticker_data(
        self, ticker: str, interval: str = "daily", backfill: bool = False
    ) -> pd.DataFrame:
        """
        Fetch and return the data for a given ticker and aggregate it based on the specified interval.

        Args:
            ticker (str): The stock ticker symbol for which to fetch the data.
            interval (str, optional): The interval for data aggregation. Defaults to 'daily'.
                                       Supported values: 'daily', 'weekly', 'monthly'.

        Returns:
            DataFrame: A pandas DataFrame containing the aggregated data.
        """
        original_df = self._fetch_data(ticker)

        if backfill:
            self.backfill = Backfill()
            backfill_ticker = self.backfill.lookup_backfill_ticker(ticker)
            if backfill_ticker:
                backfill_df = self._fetch_data(backfill_ticker)
                combined_df = DFUtil.splice(original_df, backfill_df)
            else:
                combined_df = original_df
        else:
            combined_df = original_df

        # combined_df['ticker'] = ticker # Assign the original ticker to all rows
        # combined_df.loc[combined_df.index < original_df.index.min(), 'ticker'] = backfill_ticker # Update ticker for backfill rows

        if interval == "daily":
            # No aggregation is needed if daily data is requested
            return combined_df
        elif interval == "weekly":
            # Aggregate data on a weekly basis
            return combined_df.resample("W").last()
        elif interval == "monthly":
            # Aggregate data on a monthly basis, similar to get_monthly_data
            return combined_df.resample("ME").last()
        else:
            raise ValueError(
                f"Unsupported interval: {interval}. Supported intervals are 'daily', 'weekly', 'monthly'."
            )

    def _fetch_data(self, ticker: str) -> pd.DataFrame:
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

        # Check if data is cached
        if CacheUtil.is_cached(cache_path):
            cached_df = CacheUtil.load_from_cache(cache_path)
            if CacheUtil.is_stale(cache_path) or self.force_refresh:
                # In theory we could just fetch the data from the source
                # and replace the cache with the latest version. However,
                # I want to merge the new data with the old data to avoid
                # losing any rows that might not come back from the source.
                # This approach basically allows us to accumulate data over time
                # and avoids losing data if a data source has limitations on how
                # much data is returned.

                # Fetch and format the latest data from the source
                latest_df = self._fetch_and_process_data(ticker)

                # Merge updates from latest into cached
                merged_df = DFUtil.merge(cached_df, latest_df)

                # Cache the merged data
                CacheUtil.save_to_cache(cache_path, merged_df)

                return merged_df
            else:
                return cached_df
        else:
            # Fetch and format the latest data from the source
            latest_df = self._fetch_and_process_data(ticker)

            # Cache the fetched data
            CacheUtil.save_to_cache(cache_path, latest_df)

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
        # Add the ticker as a column. Usefill when backfilled data is added.
        df["ticker"] = ticker

        # Rename columns
        df = df.rename(columns=self.COLUMN_MAPPINGS)

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
