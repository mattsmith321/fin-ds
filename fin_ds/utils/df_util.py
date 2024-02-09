import pandas as pd


class DFUtil:
    @staticmethod
    def merge(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        """
        Merges the df2 differences (updates and additions) into df1.

        Parameters:
        df1: The base DataFrame to be blended.
        df2: The DataFrame to blend with df1.

        Returns:
        pd.DataFrame: The blended DataFrame.
        """
        # Update df1 in-place with changed values from df2
        df1.update(df2)

        # Append new rows in df2 to df1
        new_rows = df2.loc[~df2.index.isin(df1.index)]
        if not new_rows.empty:
            df1 = pd.concat([df1, new_rows])

        # Re-sort df1 based on its index
        df1 = df1.sort_index()

        return df1
