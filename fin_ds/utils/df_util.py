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

        # Assuming df2 is your DataFrame
        float_columns = df1.select_dtypes(include=["float64"]).columns

        # For some reason, EODHD data was throwing warnings:
        # FutureWarning: Setting an item of incompatible dtype is deprecated and will raise in a future error of pandas.
        # Value '[...]' has dtype incompatible with float64, please explicitly cast to a compatible dtype first.
        # But the data was already float64, so I'm casting it again to float64 to suppress the warning.
        # for col in float_columns:
        #     if col in df2.columns:
        #         df2[col] = pd.to_numeric(df2[col], errors="coerce").astype("float64")

        # Update df1 in-place with changed values from df2
        df1.update(df2)

        # Use infer_objects to fix types post-update to avoid FutureWarning
        # Downcasting behavior in Series and DataFrame methods 'where', 'mask', and 'clip' is deprecated.
        # df1 = df1.infer_objects(copy=False)

        # Explicitly cast float columns to float64 post-update
        # df1[float_columns] = df1[float_columns].astype("float64")

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

        # Find the overlapping date(s), if any
        overlapping_indices = backfill_df.index.intersection(original_df.index)

        if overlapping_indices.empty:
            # If no overlap, no adjustment ratio needed
            adjustment_ratio = None  # Just for debugging or additional logging if needed
        else:
            # If there is an overlap, take the first common date as the splice point
            splice_point = overlapping_indices[0]

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
