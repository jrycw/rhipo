import polars as pl


def _exprize(elem: pl.Expr | str):
    if isinstance(elem, pl.Expr):
        return elem.cast(pl.Utf8)
    return pl.lit(str(elem))


def cols_merge_as_str(*elems: pl.Expr | str, alias: str = "merged_col") -> pl.Expr:
    """
    Parameters
    ----------
    elems
        str or Polars expressions.
    alias
        alias for the final Polars expressions.

    Returns:
    ----------
    pl.Expr
        Polars expressions

    Examples
    --------
    ```{python}
    import polars as pl
    from rhipo.utils import cols_merge_as_str

    df = pl.DataFrame({"col1": ["a"], "col2": ["b"]})
    (df.select(cols_merge_as_str(pl.col("col1"), "^_^", pl.col("col2"))))
    ```
    """
    if not elems:
        raise ValueError("No expressions are given")
    cols = None
    for elem in elems:
        if cols is None:
            cols = _exprize(elem)
            continue
        cols = cols.add(_exprize(elem))
    return cols.alias(alias)
