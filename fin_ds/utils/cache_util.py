import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union

import pandas as pd


logger = logging.getLogger(__name__)


class CacheUtil:
    """
    Utility class for caching data files.
    Provides methods for determining cache paths, checking cache existence,
    loading data from cache, and saving data to cache.
    """

    DEFAULT_CACHE_PATH_FORMAT = "fin-ds-cache/{data_source}-{ticker}.csv"

    @classmethod
    def cache_path(
        cls, data_source: str, ticker: str, cache_path_format: Union[str, None] = None
    ) -> Path:
        """
        Generates a cache path for the given data source and ticker.

        Parameters:
        - data_source: The source of the financial data.
        - ticker: The ticker symbol for the financial instrument.
        - cache_path_format: Optional format for the cache path.

        Returns:
        - A Path object representing the cache path.
        """
        if cache_path_format is None:
            cache_path_format = cls.DEFAULT_CACHE_PATH_FORMAT

        formatted_path_str = cache_path_format.format(
            data_source=data_source, ticker=ticker
        )

        return Path(formatted_path_str)

    @staticmethod
    def is_cached(cache_path: Path) -> bool:
        """
        Checks if data for a given path is cached.

        Parameters:
        - cache_path: The Path object to check for in the cache.

        Returns:
        - True if the cache exists, False otherwise.
        """
        logger.debug(f"Checking cache for: {cache_path}")
        is_cached = cache_path.exists()
        if is_cached:
            logger.info(f"Cache hit for: {cache_path}")
        else:
            logger.info(f"Cache miss for: {cache_path}")
        return is_cached

    @staticmethod
    def is_stale(cache_path: Path, max_age_hours: int = 12) -> bool:
        """
        Checks if the cache data is stale and needs to be refreshed based on its age.

        Parameters:
        - cache_path: The Path object representing the cache file.
        - max_age_hours: The maximum allowed age of the cache file in hours.

        Returns:
        - True if the cache data is stale, False otherwise.
        """
        now = datetime.now()
        mod_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        file_age = now - mod_time
        return file_age > timedelta(hours=max_age_hours)

    @staticmethod
    def load_from_cache(cache_path: Path) -> pd.DataFrame:
        """
        Loads data from cache.

        Parameters:
        - cache_path: The Path object from which to load the data.

        Returns:
        - The data loaded from the cache as a pandas DataFrame.
        """
        logger.debug(f"Loading data from cache: {cache_path}")
        start_time = time.time()
        try:
            data = pd.read_csv(cache_path, index_col=0, parse_dates=True)
            logger.info(f"Data successfully loaded from {cache_path}")
        except Exception as e:
            logger.error(
                f"Failed to load data from cache: {cache_path}. Error: {e}",
                exc_info=True,
            )
            raise
        elapsed_time = time.time() - start_time
        logger.debug(f"load_from_cache() executed in {elapsed_time:.2f} seconds.")
        return data

    @staticmethod
    def save_to_cache(cache_path: Path, df: pd.DataFrame) -> None:
        """
        Saves data to cache.

        Parameters:
        - cache_path: The Path object where the data should be saved.
        - data: The pandas DataFrame to save to cache.
        """
        start_time = time.time()
        logger.info(f"Attempting to save data to cache: {cache_path}")
        try:
            cache_directory = cache_path.parent
            cache_directory.mkdir(parents=True, exist_ok=True)
            df.to_csv(cache_path)
            logger.info(f"Data successfully saved to {cache_path}")
        except Exception as e:
            logger.error(f"Failed to save data to cache: {e}", exc_info=True)
            raise
        elapsed_time = time.time() - start_time
        logger.debug(f"save_to_cache() executed in {elapsed_time:.2f} seconds.")
