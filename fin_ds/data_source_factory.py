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
    _data_sources = {}

    @classmethod
    def _get_data_sources(cls):
        """
        Gets available data source classes in the /DataSources folder.
        Updates the _data_sources dictionary directly.
        """
        data_sources_dir = Path(__file__).resolve().parent / "data_sources"
        if not data_sources_dir.exists():
            raise FileNotFoundError(f"The directory {data_sources_dir} does not exist.")

        for _, module_name, _ in pkgutil.iter_modules([str(data_sources_dir)]):
            try:
                module = importlib.import_module(
                    f".data_sources.{module_name}", __package__
                )
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if (
                        isinstance(attribute, type)
                        and issubclass(attribute, BaseDataSource)
                        and attribute is not BaseDataSource
                    ):
                        cls._data_sources[
                            attribute.__name__.removesuffix("DataSource")
                        ] = attribute
            except Exception as e:
                logger.error(f"Error loading data source module '{module_name}': {e}")

    @classmethod
    @property
    def data_sources(cls):
        """
        Ensures data sources are loaded and returns their names.
        """
        if not cls._data_sources:
            cls._get_data_sources()
        return list(cls._data_sources.keys())

    def __new__(cls, data_source_name, force_refresh=False):
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
            cls._get_data_sources()

        # Check if the data source class is already registered
        if data_source_name in cls._data_sources:
            data_source_class = cls._data_sources[data_source_name]
            api_key = None
            if data_source_class.api_key_required:
                api_key_name = f"{data_source_name.replace(' ', '').upper()}_API_KEY"
                api_key = config(api_key_name)
            return data_source_class(data_source_name, api_key, force_refresh)

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

        # Automatically parse the class name, removing 'DataSource' suffix if present
        class_name = data_source_class.__name__.removesuffix("DataSource")

        cls._data_sources[class_name] = data_source_class

    @classmethod
    def get_data_source_instance(cls, data_source_name, *args, **kwargs):
        """
        Creates a new instance of a data source class based on the given data source name.

        Args:
            data_source_name (str): The name of the data source.
            *args, **kwargs: Arguments to pass to the data source class constructor.

        Returns:
            An instance of the data source class.

        Raises:
            ValueError: If an invalid data source name is provided.
        """
        if not cls._data_sources:  # Ensure data sources are loaded
            cls._get_data_sources()

        if data_source_name not in cls._data_sources:
            raise ValueError(f"Invalid data provider: {data_source_name}")

        data_source_class = cls._data_sources[data_source_name]
        return data_source_class(*args, **kwargs)  # Instantiate the class
