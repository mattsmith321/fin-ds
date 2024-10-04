import pytest
import pandas as pd
from fin_ds.data_source_factory import DataSourceFactory


# Marking these tests as integration tests
class TestYFinanceDataSource:

    @pytest.fixture
    def data_source(self):
        data_source_name = "YFinance"
        return DataSourceFactory(data_source_name)

    @pytest.mark.integration
    def test_fetch_data_from_source(self, data_source):
        ticker = "AAPL"
        df = data_source._fetch_data_from_source(ticker)

        # Verify that the returned value is a DataFrame
        assert isinstance(df, pd.DataFrame), "The returned data should be a DataFrame"

        # Check that the DataFrame has the expected columns
        expected_columns = set(["Open", "High", "Low", "Close", "Adj Close", "Volume"])
        assert expected_columns.issubset(
            df.columns
        ), f"The DataFrame should have the expected columns. Actual columns: {list(df.columns)}"

    @pytest.mark.integration
    def test_column_mapping(self, data_source):
        ticker = "MSFT"
        df = data_source._fetch_data_from_source(ticker)
        df_mapped = data_source._preprocess_data(ticker, df)

        # Verify that columns have been mapped correctly
        expected_columns = data_source.COLUMN_ORDER
        assert (
            list(df_mapped.columns) == expected_columns
        ), f"The columns should match the expected order and names. Actual columns: {list(df_mapped.columns)}"

        # Verify that the ticker column is filled correctly
        assert (
            df_mapped["ticker"] == ticker
        ).all(), "All rows should have the correct ticker value"

    @pytest.mark.integration
    def test_get_eod_data_daily(self, data_source):
        ticker = "NVDA"
        df = data_source.get_eod_data(ticker, interval="daily")

        # Verify that the returned value is a DataFrame
        assert isinstance(df, pd.DataFrame), "The returned data should be a DataFrame"

        # Check that the DataFrame has the expected columns
        expected_columns = data_source.COLUMN_ORDER
        assert (
            list(df.columns) == expected_columns
        ), f"The columns should match the expected order and names. Actual columns: {list(df.columns)}"

    @pytest.mark.integration
    def test_get_eod_data_weekly(self, data_source):
        ticker = "AMZN"
        df = data_source.get_eod_data(ticker, interval="weekly")

        # Verify that the returned value is a DataFrame
        assert isinstance(df, pd.DataFrame), "The returned data should be a DataFrame"

        # Check that the DataFrame is resampled to weekly frequency
        assert (
            df.index.freq == "W-SUN" or df.index.freq == "W"
        ), "The DataFrame should be resampled to weekly frequency"

    @pytest.mark.integration
    def test_get_eod_data_monthly(self, data_source):
        ticker = "META"
        df = data_source.get_eod_data(ticker, interval="monthly")

        # Verify that the returned value is a DataFrame
        assert isinstance(df, pd.DataFrame), "The returned data should be a DataFrame"

        # Check that the DataFrame is resampled to monthly frequency
        assert df.index.freq == "ME", "The DataFrame should be resampled to monthly frequency"
