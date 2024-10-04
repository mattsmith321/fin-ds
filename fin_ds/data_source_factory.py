import importlib
import importlib.util
import logging
import pkgutil
from pathlib import Path

from decouple import config

from fin_ds.data_sources.base_data_source import BaseDataSource

# module-level (or global-level) variables/constants
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# List of data sources to register
DATA_SOURCES_TO_REGISTER = [
    "alphavantage",
    "eodhd",
    "nasdaqdatalink",
    "tiingo",
    "yfinance",
]


class DataSourceFactory:

    # Class variable for caching discovered data source classes
    _data_sources = {}

    @classmethod
    def _register_data_sources(cls):
        """
        Imports data source modules to trigger self-registration.
        """
        for module_name in DATA_SOURCES_TO_REGISTER:
            __import__(f"fin_ds.data_sources.{module_name}")

    @classmethod
    def get_data_source_names(cls):
        """
        Ensures data sources are loaded and returns their names.
        """
        if not cls._data_sources:
            cls._register_data_sources()
        return list(cls._data_sources.keys())

    def __new__(cls, data_source_name="YFinance"):
        """
        Create a new instance of a data source class based on the given data source name.

        Args:
            data_source_name (str): The name of the data source.
            force_refresh (bool, optional): Whether to force a data refresh. Defaults to False.

        Returns:
            object: An instance of the data source class.

        Raises:
            ValueError: If an invalid data source name is provided.
        """
        if not cls._data_sources:  # Ensure data sources are loaded
            cls._register_data_sources()

        # Check if the data source class is already registered
        if data_source_name in cls._data_sources:
            data_source_class = cls._data_sources[data_source_name]
            api_key = None
            if data_source_class.api_key_required:
                api_key_name = f"{data_source_name.replace(' ', '').upper()}_API_KEY"
                api_key = config(api_key_name)
            return data_source_class(data_source_name, api_key)

        # Fallback to the original dynamic import logic if not found in registered sources
        # This part might need adjustment or removal depending on whether you still want to support dynamic loading
        raise ValueError(f"Data source '{data_source_name}' not registered.")

    @classmethod
    def register_data_source(cls, data_source_class):
        """
        Registers a custom data source class.

        Args:
            name (str): The name of the data source to register.
            data_source_class (type): The class of the data source to register.
        """
        if not issubclass(data_source_class, BaseDataSource):
            raise ValueError(f"Data source class must subclass BaseDataSource")

        # Ensure built-in data sources are loaded
        if not cls._data_sources:
            cls._register_data_sources()

        # Automatically parse the class name, removing 'DataSource' suffix if present
        class_name = data_source_class.__name__.removesuffix("DataSource")

        cls._data_sources[class_name] = data_source_class
