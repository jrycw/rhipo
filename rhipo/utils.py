import polars as pl


def _exprize(elem: pl.Expr | str):
    if isinstance(elem, pl.Expr):
        return elem.cast(pl.Utf8)
    return pl.lit(str(elem))


def cols_merge_as_str(*elems: pl.Expr | str, alias: str = "merged_col") -> pl.Expr:
    if not elems:
        raise ValueError("No expressions are given")
    cols = None
    for elem in elems:
        if cols is None:
            cols = _exprize(elem)
            continue
        cols = cols.add(_exprize(elem))
    return cols.alias(alias)
