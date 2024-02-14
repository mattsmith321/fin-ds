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
            df1 = pd.concat([df1, new_rows]).sort_index()

        return df1

    @staticmethod
    def splice(original_df, backfill_df, column_name="adj_close"):
        # Calculate daily percent change for both dataframes
        original_df["pct_change"] = original_df[column_name].pct_change()
        backfill_df["pct_change"] = backfill_df[column_name].pct_change()

        # Find the last overlapping date, which is our splice point
        splice_point = backfill_df.index.intersection(original_df.index)[0]

        # Calculate the adjustment ratio
        adjustment_ratio = (
            original_df.loc[splice_point, column_name]
            / backfill_df.loc[splice_point, column_name]
        )

        # Adjust the backfill dataframe 'adj_close' values
        backfill_df[column_name] *= adjustment_ratio

        # Drop the 'pct_change' column as it's no longer needed
        original_df.drop("pct_change", axis=1, inplace=True)
        backfill_df.drop("pct_change", axis=1, inplace=True)

        # Combine the two datasets
        # We keep the original data where it exists, and append the backfill data up to the splice point
        spliced_df = pd.concat(
            [backfill_df[backfill_df.index < original_df.index.min()], original_df]
        )

        return spliced_df
