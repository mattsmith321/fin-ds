import pandas as pd
import pytest
from datetime import datetime, timedelta
from pathlib import Path
from unittest import mock
from fin_ds.utils.cache_util import CacheUtil


def test_cache_path_default_format():
    path = CacheUtil.cache_path("YFinance", "AAPL")
    expected_path = "fin-ds-cache\\YFinance-AAPL.csv"
    assert str(path) == expected_path


def test_cache_path_custom_format():
    custom_format = "custom-cache/{data_source}\\{ticker}.csv"
    path = CacheUtil.cache_path("YFinance", "AAPL", custom_format)
    expected_path = "custom-cache\\YFinance\\AAPL.csv"
    assert str(path) == expected_path


def test_is_cached_true():
    mock_path = mock.Mock(spec=Path)
    mock_path.exists.return_value = True
    assert CacheUtil.is_cached(mock_path) is True


def test_is_cached_false():
    mock_path = mock.Mock(spec=Path)
    mock_path.exists.return_value = False
    assert CacheUtil.is_cached(mock_path) is False


def test_is_stale_not_stale():
    mock_path = mock.Mock(spec=Path)
    mock_path.stat.return_value.st_mtime = (datetime.now() - timedelta(hours=1)).timestamp()
    assert CacheUtil.is_stale(mock_path, max_cache_age_in_hours=12) is False


def test_is_stale_true():
    mock_path = mock.Mock(spec=Path)
    mock_path.stat.return_value.st_mtime = (datetime.now() - timedelta(hours=13)).timestamp()
    assert CacheUtil.is_stale(mock_path, max_cache_age_in_hours=12) is True


@mock.patch("pandas.read_csv")
def test_load_from_cache(mock_read_csv):
    mock_path = mock.Mock(spec=Path)
    mock_df = pd.DataFrame({"A": [1, 2], "B": [3.0, 4.0]})
    mock_read_csv.return_value = mock_df

    result = CacheUtil.load_from_cache(mock_path)
    pd.testing.assert_frame_equal(result, mock_df)
    mock_read_csv.assert_called_once_with(mock_path, index_col=0, parse_dates=True)


@mock.patch("pandas.DataFrame.to_csv")
def test_save_to_cache(mock_to_csv):
    mock_path = mock.Mock(spec=Path)
    mock_df = pd.DataFrame({"A": [1, 2], "B": [3.0, 4.0]})

    CacheUtil.save_to_cache(mock_path, mock_df)
    mock_path.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_to_csv.assert_called_once_with(mock_path)


@mock.patch("pandas.read_csv", side_effect=Exception("Failed to read"))
def test_load_from_cache_error(mock_read_csv):
    mock_path = mock.Mock(spec=Path)
    with pytest.raises(Exception, match="Failed to read"):
        CacheUtil.load_from_cache(mock_path)


@mock.patch("pandas.DataFrame.to_csv", side_effect=Exception("Failed to write"))
def test_save_to_cache_error(mock_to_csv):
    mock_path = mock.Mock(spec=Path)
    mock_df = pd.DataFrame({"A": [1, 2], "B": [3.0, 4.0]})

    with pytest.raises(Exception, match="Failed to write"):
        CacheUtil.save_to_cache(mock_path, mock_df)
