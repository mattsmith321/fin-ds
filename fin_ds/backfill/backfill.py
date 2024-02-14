import csv
import os


class Backfill:
    DEFAULT_BACKFILL_CSV = "fin_ds\\backfill\\backfill.csv"

    def __init__(self, backfill_path: str = None):
        """
        Initialize the TickerCrosswalk with data from a CSV file.
        If no path is provided, it uses the default '.backfill.csv' in the current directory.

        Args:
            csv_file_path (str, optional): Path to the CSV file containing ticker mappings.
        """
        # Set the default file path if none is provided
        if backfill_path is None:
            # You can define the default location of your .backfill.csv file here
            backfill_path = os.path.join(os.getcwd(), self.DEFAULT_BACKFILL_CSV)

        if os.path.exists(backfill_path):
            backfill_path = backfill_path
        else:
            raise FileNotFoundError(f"Backfill CSV file not found ({backfill_path}).")

        self.crosswalk = self.load_crosswalk(backfill_path)

    def load_crosswalk(self, csv_file_path: str) -> dict:
        """
        Load the ticker mappings from a CSV file.

        Args:
            csv_file_path (str): Path to the CSV file.

        Returns:
            dict: A dictionary with original tickers as keys and backfill tickers as values.
        """
        crosswalk = {}
        with open(csv_file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip the header row
            for row in reader:
                if len(row) >= 2:
                    original_ticker, backfill_ticker = row[0].strip(), row[1].strip()
                    crosswalk[original_ticker] = backfill_ticker
        return crosswalk

    def lookup_backfill_ticker(self, original_ticker: str) -> str:
        """
        Look up the backfill ticker symbol for a given original ticker symbol.

        Args:
            original_ticker (str): The original ticker symbol.

        Returns:
            str: The backfill ticker symbol, if found. Returns None if no mapping exists.
        """
        return self.crosswalk.get(original_ticker, None)
