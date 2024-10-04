import sys
import tempfile
from pathlib import Path
from unittest import mock

from fin_ds.data_source_factory import DataSourceFactory
from fin_ds.data_sources.base_data_source import BaseDataSource


# @mock.patch("fin_ds.data_source_factory.pkgutil.iter_modules")
# @mock.patch("fin_ds.data_source_factory.importlib.import_module")
# def test_load_data_sources(mock_import_module, mock_iter_modules):
#     # Mock the data sources directory to return two modules
#     mock_iter_modules.return_value = [(None, "module1", None), (None, "module2", None)]

#     # Mock module1 and module2 to contain BaseDataSource subclasses
#     mock_module1 = mock.Mock()
#     mock_class1 = mock.Mock()
#     mock_class1.__name__ = "CustomDataSource"
#     mock_class1.api_key_required = False
#     mock_module1.CustomDataSource = mock_class1

#     mock_module2 = mock.Mock()
#     mock_class2 = mock.Mock()
#     mock_class2.__name__ = "AnotherDataSource"
#     mock_class2.api_key_required = False
#     mock_module2.AnotherDataSource = mock_class2

#     mock_import_module.side_effect = [mock_module1, mock_module2]

#     DataSourceFactory._data_sources = {}  # Clear the cache
#     DataSourceFactory._load_data_sources()

#     assert "Custom" in DataSourceFactory._data_sources
#     assert "Another" in DataSourceFactory._data_sources


def test_default_data_source():
    """Test the initialization of the DataSourceFactory with a valid data source."""
    ds = DataSourceFactory()
    df = ds.get_eod_data("AAPL")
    assert df is not None
    assert len(df) > 0  # Ensure data was returned


def test_alphavantage_data_source():
    """Test the initialization of the DataSourceFactory with a valid data source."""
    ds = DataSourceFactory("AlphaVantage")
    df = ds.get_eod_data("AAPL")
    assert df is not None
    assert len(df) > 0  # Ensure data was returned


def test_eodhd_data_source():
    """Test the initialization of the DataSourceFactory with a valid data source."""
    ds = DataSourceFactory("EODHD")
    df = ds.get_eod_data("AAPL")
    assert df is not None
    assert len(df) > 0  # Ensure data was returned


def test_nasdaqdatalink_data_source():
    """Test the initialization of the DataSourceFactory with a valid data source."""
    ds = DataSourceFactory("NasdaqDataLink")
    df = ds.get_eod_data("AAPL")
    assert df is not None
    assert len(df) > 0  # Ensure data was returned


def test_tiingo_data_source():
    """Test the initialization of the DataSourceFactory with a valid data source."""
    ds = DataSourceFactory("Tiingo")
    df = ds.get_eod_data("AAPL")
    assert df is not None
    assert len(df) > 0  # Ensure data was returned


def test_yfinance_data_source():
    """Test the initialization of the DataSourceFactory with a valid data source."""
    ds = DataSourceFactory("YFinance")
    df = ds.get_eod_data("AAPL")
    assert df is not None
    assert len(df) > 0  # Ensure data was returned


def test_get_eod_data():
    """Test that ticker data is fetched correctly."""
    ds = DataSourceFactory("YFinance")
    df = ds.get_eod_data("AAPL")
    assert df is not None
    assert len(df) > 0  # Ensure data was returned
