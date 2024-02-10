import logging
from pathlib import Path

import pandas as pd
from pandas.tseries.offsets import MonthEnd

from fin_ds.data_sources.base_data_source import BaseDataSource

# module-level (or global-level) variables/constants
logger = logging.getLogger(__name__)


class PortfolioVisualizerDataSource(BaseDataSource):
    # Set this to False if no api key is required
    api_key_required = False

    INPUT_PATH_FORMAT = "fin-ds-input/{data_source}-{ticker}.xlsx"

    COLUMN_MAPPINGS = {}

    COLUMN_ORDER = [
        "adj_close",
    ]

    def __init__(self, name, api_key, force_refresh=False):
        # Call the base class __init__
        super().__init__(name, force_refresh)

    def _fetch_data_from_source(self, ticker) -> pd.DataFrame:
        # Step 1: Read the entire Excel file

        formatted_path_str = self.INPUT_PATH_FORMAT.format(
            data_source=self.name, ticker=ticker
        )

        file_path = Path(formatted_path_str)

        # cache_filename = CacheUtil.cache_filename(ticker, self.name)
        # file_path = os.path.join(
        #     settings.DATA_DIR, f"{cache_filename.replace('.csv', '.xlsx')}"
        # )
        df = pd.read_excel(file_path, header=None)  # No header initially

        # Step 2: Find the row containing 'Monthly Returns'
        identifier = "Monthly Returns"
        identifier_row = df[df[0] == identifier].index[0]

        # Step 3: Determine the ending row (first empty row after the identifier)
        # Assuming blank lines are NaN in the first column
        ending_row = df[df[0].isna() & (df.index > identifier_row)].index[0]

        # Step 4: Read the actual data
        data_start_row = identifier_row + 1
        df = pd.read_excel(
            file_path,
            skiprows=data_start_row,
            nrows=ending_row - data_start_row,
            header=0,
            usecols="A:E",
        )

        # Create 'date' column from the Year and Month columns
        df["date"] = pd.to_datetime(
            df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2)
        )

        # Adjust to the last day of the month
        df["date"] = df["date"] + MonthEnd(0)

        df = df.set_index("date")

        # Rename the last column to a consistent name
        df.rename(columns={df.columns[4]: "return"}, inplace=True)

        # Calculate the adjusted close since we don't have it
        df = pd.DataFrame({"adj_close": (1 + df["return"]).cumprod() * 1})

        return df
