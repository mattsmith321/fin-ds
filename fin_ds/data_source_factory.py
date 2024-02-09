import importlib
import logging
import pkgutil
from pathlib import Path

from decouple import config

from fin_ds.data_sources.base_data_source import BaseDataSource

# module-level (or global-level) variables/constants
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DataSourceFactory:
    MODULE_NAME_FORMAT = "fin_ds.data_sources.{data_source_name}"

    # Class variable for caching discovered data source classes
    _data_sources = None

    @classmethod
    def _get_data_sources(cls):
        """
        Gets available data source classes in the /DataSources folder.

        Raises:
            FileNotFoundError: If the /DataSources directory does not exist.

        Returns:
            list[str]: A list of class names of available data sources.
        """

        # Assuming /DataSources is a subdirectory of the directory containing this script
        data_sources_dir = Path(__file__).resolve().parent / "data_sources"

        # Ensure the directory exists
        if not data_sources_dir.exists():
            raise FileNotFoundError(f"The directory {data_sources_dir} does not exist.")

        data_sources = []

        # Iterate over all *.py files in the directory
        for _, module_name, _ in pkgutil.iter_modules([str(data_sources_dir)]):
            # The module name is already formatted as needed for import_module
            try:
                module = importlib.import_module(
                    f".data_sources.{module_name}", __package__
                )
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    # Assuming BaseDataSource is the base class for all data sources
                    if (
                        isinstance(attribute, type)
                        and issubclass(attribute, BaseDataSource)
                        and attribute is not BaseDataSource
                    ):
                        # Remove 'DataSource' from the class name for simplified access
                        simplified_name = attribute.__name__.removesuffix("DataSource")

                        data_sources.append(simplified_name)
            except Exception as e:
                # Log or print the error depending on your error handling strategy
                logger.error(f"Error loading data source module '{module_name}': {e}")

        return data_sources

    @classmethod
    @property
    def data_sources(cls):
        """
        A class-level property that dynamically loads and caches available data source classes.

        Returns:
            list[str]: A list of class names of available data sources.
        """
        if cls._data_sources is None:
            cls._data_sources = cls._get_data_sources()
        return cls._data_sources

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
        if data_source_name not in self.data_sources:
            raise ValueError(f"Invalid data provider: {data_source_name}")

        module_name = self.MODULE_NAME_FORMAT.format(
            data_source_name=data_source_name.lower()
        )
        class_name = f"{data_source_name}DataSource"

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
