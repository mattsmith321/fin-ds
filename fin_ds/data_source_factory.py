import importlib
import logging

from decouple import config

# module-level (or global-level) variables/constants
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DataSourceFactory:
    # Constants for data source settings
    DATA_SOURCES = [
        "Alpha Vantage",
        "EODHD",
        "Nasdaq",
        "Portfolio Visualizer",
        "Tiingo",
        "Yahoo Finance",
    ]
    MODULE_NAME_FORMAT = "fin_ds.data_sources.{data_source_name}"

    def __new__(self, data_source_name, force_refresh=False):
        """
        Create a new instance of a data source class based on the given data source name.

        Args:
            data_source_name (str): The name of the data source.
            force_refresh (bool, optional): Whether to force a data refresh. Defaults to False.

        Returns:
            object: An instance of the data source class.

        Raises:
            ValueError: If an invalid data source name is provided.
            ImportError: If the data source module or class cannot be imported.
        """
        if data_source_name not in self.DATA_SOURCES:
            raise ValueError(f"Invalid data provider: {data_source_name}")

        module_name = self.MODULE_NAME_FORMAT.format(
            data_source_name=data_source_name.replace(" ", "_").lower()
        )
        class_name = f"{data_source_name.replace(' ', '')}DataSource"

        try:
            # Dynamically import the data source module
            data_source_module = importlib.import_module(module_name)

            # Get the data source class from the module
            data_source_class = getattr(data_source_module, class_name)

        except (ImportError, AttributeError) as e:
            raise ImportError(f"Could not load data source '{data_source_name}': {e}")

        api_key_name = f"{data_source_name.replace(' ', '').upper()}_API_KEY"

        if data_source_class.api_key_required:
            api_key = config(api_key_name)
        else:
            api_key = None

        return data_source_class(data_source_name, api_key, force_refresh)
