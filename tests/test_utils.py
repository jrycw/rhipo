import polars as pl
import pytest
from polars.testing import assert_frame_equal
from rhipo.utils import cols_merge_as_str


def test_cols_merge_as_str_raises():
    with pytest.raises(ValueError) as exc_info:
        cols_merge_as_str()

    assert "No expressions are given" in exc_info.value.args[0]


def test_cols_merge_as_str():
    df = pl.DataFrame(
        {
            "col1": [1, 2, 3],
            "col2": ["dogs", "cats", "goats"],
            "col3": ["bark", "meow", "bleat"],
            "col4": ["!", "!!", "!!!"],
        }
    )
    col_expr = cols_merge_as_str(
        pl.col("col1"),
        " ",
        "*",
        pl.col("col2"),
        "*",
        " ",
        pl.col("col3"),
        pl.col("col4"),
    )
    selected = df.select(col_expr)
    expected = pl.DataFrame(
        {
            col_expr.meta.output_name(): [
                "1 *dogs* bark!",
                "2 *cats* meow!!",
                "3 *goats* bleat!!!",
            ]
        }
    )

    assert_frame_equal(selected, expected)
