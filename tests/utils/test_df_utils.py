import pandas as pd
from fin_ds.utils.df_util import DFUtil


def test_merge_basic():
    df1 = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}, index=[0, 1, 2])

    df2 = pd.DataFrame({"A": [10, 20], "B": [40, 50]}, index=[1, 2])

    expected = pd.DataFrame({"A": [1, 10, 20], "B": [4, 40, 50]}, index=[0, 1, 2])

    result = DFUtil.merge(df1, df2)
    pd.testing.assert_frame_equal(result, expected)


def test_merge_with_new_rows():
    df1 = pd.DataFrame({"A": [1, 2], "B": [4, 5]}, index=[0, 1])

    df2 = pd.DataFrame({"A": [3, 4], "B": [6, 7]}, index=[2, 3])

    expected = pd.DataFrame({"A": [1, 2, 3, 4], "B": [4, 5, 6, 7]}, index=[0, 1, 2, 3])

    result = DFUtil.merge(df1, df2)
    pd.testing.assert_frame_equal(result, expected)


def test_merge_empty():
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()

    expected = pd.DataFrame()
    result = DFUtil.merge(df1, df2)
    pd.testing.assert_frame_equal(result, expected)


def test_splice_basic():
    original_df = pd.DataFrame(
        {
            "adj_close": [100, 105, 110],
        },
        index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
    )

    backfill_df = pd.DataFrame(
        {
            "adj_close": [90, 95, 100],
        },
        index=pd.to_datetime(["2023-12-29", "2023-12-30", "2024-01-01"]),
    )

    expected = pd.DataFrame(
        {
            "adj_close": [90, 95, 100.0, 105.0, 110.0],
        },
        index=pd.to_datetime(
            ["2023-12-29", "2023-12-30", "2024-01-01", "2024-01-02", "2024-01-03"]
        ),
    )

    result = DFUtil.splice(original_df, backfill_df, column_name="adj_close")
    pd.testing.assert_frame_equal(result, expected)


def test_splice_adjustment():
    original_df = pd.DataFrame(
        {
            "adj_close": [200, 210],
        },
        index=pd.to_datetime(["2024-01-01", "2024-01-02"]),
    )

    backfill_df = pd.DataFrame(
        {
            "adj_close": [90, 100],
        },
        index=pd.to_datetime(["2023-12-31", "2024-01-01"]),
    )

    # The adjustment ratio is 200 / 100 = 2, so backfill_df should be multiplied by 2
    expected = pd.DataFrame(
        {
            "adj_close": [180.0, 200.0, 210.0],
        },
        index=pd.to_datetime(["2023-12-31", "2024-01-01", "2024-01-02"]),
    )

    result = DFUtil.splice(original_df, backfill_df, column_name="adj_close")
    pd.testing.assert_frame_equal(result, expected)


def test_splice_no_overlap():
    original_df = pd.DataFrame(
        {
            "adj_close": [200, 210],
        },
        index=pd.to_datetime(["2024-01-01", "2024-01-02"]),
    )

    backfill_df = pd.DataFrame(
        {
            "adj_close": [100, 105],
        },
        index=pd.to_datetime(["2023-12-29", "2023-12-30"]),
    )

    expected = pd.DataFrame(
        {
            "adj_close": [100, 105, 200, 210],
        },
        index=pd.to_datetime(["2023-12-29", "2023-12-30", "2024-01-01", "2024-01-02"]),
    )

    result = DFUtil.splice(original_df, backfill_df, column_name="adj_close")
    pd.testing.assert_frame_equal(result, expected)
