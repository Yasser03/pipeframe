"""
Reshape operations for PipeFrame - transform data between wide and long formats.

This module provides functions for reshaping DataFrames, including:
- Pivoting (wide to long and long to wide)
- Melting and stacking
- Separating and uniting columns
- Tidyr-style reshaping operations
"""

from typing import Any, Callable, List, Optional, Union
from functools import partial

import pandas as pd

from ..core.dataframe import DataFrame
from ..exceptions import PipeFrameValueError, PipeFrameColumnError


# ============================================================================
# Pivot Operations
# ============================================================================


def _pivot_wider_impl(
    df: Union[DataFrame, pd.DataFrame],
    id_cols: Optional[Union[str, List[str]]] = None,
    names_from: Union[str, List[str]] = None,
    values_from: Union[str, List[str]] = None,
    values_fill: Optional[Any] = None,
    names_sep: str = "_",
    names_prefix: str = "",
) -> DataFrame:
    """
    Pivot data from long to wide format (tidyr-style).

    Transform data so that names become column names and values populate
    those columns.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame (long format)
    id_cols : str or list of str, optional
        Columns that identify observations (won't be pivoted)
    names_from : str or list of str
        Column(s) whose values will become new column names
    values_from : str or list of str
        Column(s) whose values will fill the new columns
    values_fill : scalar, optional
        Value to use for missing combinations
    names_sep : str, default '_'
        Separator for column names when using multiple names_from
    names_prefix : str, default ''
        Prefix to add to new column names

    Returns
    -------
    DataFrame
        Pivoted DataFrame (wide format)

    Raises
    ------
    PipeFrameValueError
        If required arguments are missing
    PipeFrameColumnError
        If specified columns don't exist

    Examples
    --------
    >>> # Long format
    >>> df = DataFrame({
    ...     'id': [1, 1, 2, 2],
    ...     'measure': ['height', 'weight', 'height', 'weight'],
    ...     'value': [170, 70, 180, 80]
    ... })
    >>> # Convert to wide format
    >>> wide = df >> pivot_wider(
    ...     id_cols='id',
    ...     names_from='measure',
    ...     values_from='value'
    ... )
    >>> print(wide)
    #    id  height  weight
    # 0   1     170      70
    # 1   2     180      80
    """
    if isinstance(df, DataFrame):
        data = df._data
    else:
        data = df

    if names_from is None:
        raise PipeFrameValueError("names_from is required for pivot_wider")
    if values_from is None:
        raise PipeFrameValueError("values_from is required for pivot_wider")

    # Validate columns exist
    names_from_cols = [names_from] if isinstance(names_from, str) else names_from
    values_from_cols = [values_from] if isinstance(values_from, str) else values_from

    for col in names_from_cols + values_from_cols:
        if col not in data.columns:
            raise PipeFrameColumnError(col, list(data.columns))

    if id_cols is not None:
        id_cols_list = [id_cols] if isinstance(id_cols, str) else id_cols
        for col in id_cols_list:
            if col not in data.columns:
                raise PipeFrameColumnError(col, list(data.columns))
    else:
        # Use all columns except names_from and values_from as id_cols
        id_cols_list = [
            col
            for col in data.columns
            if col not in names_from_cols and col not in values_from_cols
        ]

    # Perform pivot
    result = data.pivot(
        index=id_cols_list if id_cols_list else None,
        columns=names_from_cols if len(names_from_cols) == 1 else names_from_cols,
        values=values_from_cols if len(values_from_cols) == 1 else values_from_cols,
    )

    # Handle column names
    if isinstance(result.columns, pd.MultiIndex):
        # Flatten multi-index columns
        result.columns = [names_sep.join(map(str, col)).strip() for col in result.columns.values]

    # Add prefix if specified
    if names_prefix:
        result.columns = [names_prefix + str(col) for col in result.columns]

    # Fill missing values
    if values_fill is not None:
        result = result.fillna(values_fill)

    # Reset index to make id_cols regular columns
    result = result.reset_index()

    return DataFrame(result)


def pivot_wider(
    id_cols: Optional[Union[str, List[str]]] = None,
    names_from: Union[str, List[str]] = None,
    values_from: Union[str, List[str]] = None,
    values_fill: Optional[Any] = None,
    names_sep: str = "_",
    names_prefix: str = "",
) -> Callable:
    """
    Pivot data from long to wide format - curry-friendly wrapper for pipe operator.

    Returns
    -------
    Callable
        Function that takes a DataFrame and applies pivot_wider

    Examples
    --------
    >>> df >> pivot_wider(id_cols='id', names_from='measure', values_from='value')
    """
    return lambda df: _pivot_wider_impl(
        df, id_cols, names_from, values_from, values_fill, names_sep, names_prefix
    )


def _pivot_longer_impl(
    df: Union[DataFrame, pd.DataFrame],
    cols: Union[str, List[str], None] = None,
    cols_vary: str = "fastest",
    names_to: str = "variable",
    values_to: str = "value",
    names_prefix: str = "",
    names_sep: Optional[str] = None,
    names_pattern: Optional[str] = None,
    values_drop_na: bool = False,
) -> DataFrame:
    """
    Pivot data from wide to long format (tidyr-style).

    Transform data so that column names become values in a new column
    and the column values go into another new column.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame (wide format)
    cols : str, list of str, or None
        Columns to pivot into longer format. If None, uses all numeric columns.
    cols_vary : str, default 'fastest'
        How to vary column order in output
    names_to : str, default 'variable'
        Name of new column containing old column names
    values_to : str, default 'value'
        Name of new column containing values
    names_prefix : str, default ''
        Prefix to remove from column names
    names_sep : str, optional
        Separator to split column names
    names_pattern : str, optional
        Regex pattern to extract from column names
    values_drop_na : bool, default False
        Drop rows with NA values

    Returns
    -------
    DataFrame
        Pivoted DataFrame (long format)

    Examples
    --------
    >>> # Wide format
    >>> df = DataFrame({
    ...     'id': [1, 2],
    ...     'height': [170, 180],
    ...     'weight': [70, 80]
    ... })
    >>> # Convert to long format
    >>> long = df >> pivot_longer(
    ...     cols=['height', 'weight'],
    ...     names_to='measure',
    ...     values_to='value'
    ... )
    >>> print(long)
    #    id  measure  value
    # 0   1   height    170
    # 1   1   weight     70
    # 2   2   height    180
    # 3   2   weight     80
    """
    if isinstance(df, DataFrame):
        data = df._data.copy()
    else:
        data = df.copy()

    # Determine columns to pivot
    if cols is None:
        # Use all numeric columns
        cols = data.select_dtypes(include=["number"]).columns.tolist()
    elif isinstance(cols, str):
        cols = [cols]

    # Validate columns exist
    for col in cols:
        if col not in data.columns:
            raise PipeFrameColumnError(col, list(data.columns))

    # Get id columns (columns not being pivoted)
    id_vars = [col for col in data.columns if col not in cols]

    # Remove prefix from column names if specified
    if names_prefix:
        col_rename = {
            col: col.replace(names_prefix, "", 1) for col in cols if col.startswith(names_prefix)
        }
        data = data.rename(columns=col_rename)
        cols = [col_rename.get(col, col) for col in cols]

    # Perform melt
    result = pd.melt(
        data,
        id_vars=id_vars if id_vars else None,
        value_vars=cols,
        var_name=names_to,
        value_name=values_to,
    )

    # Drop NA values if requested
    if values_drop_na:
        result = result.dropna(subset=[values_to])

    return DataFrame(result)


def pivot_longer(
    cols: Union[str, List[str], None] = None,
    cols_vary: str = "fastest",
    names_to: str = "variable",
    values_to: str = "value",
    names_prefix: str = "",
    names_sep: Optional[str] = None,
    names_pattern: Optional[str] = None,
    values_drop_na: bool = False,
) -> Callable:
    """
    Pivot data from wide to long format - curry-friendly wrapper for pipe operator.

    Returns
    -------
    Callable
        Function that takes a DataFrame and applies pivot_longer

    Examples
    --------
    >>> df >> pivot_longer(cols=['Q1', 'Q2'], names_to='quarter', values_to='sales')
    """
    return lambda df: _pivot_longer_impl(
        df,
        cols,
        cols_vary,
        names_to,
        values_to,
        names_prefix,
        names_sep,
        names_pattern,
        values_drop_na,
    )


def pivot(
    df: Union[DataFrame, pd.DataFrame],
    index: Optional[Union[str, List[str]]] = None,
    columns: Optional[Union[str, List[str]]] = None,
    values: Optional[Union[str, List[str]]] = None,
) -> DataFrame:
    """
    Pivot DataFrame (pandas-style).

    Reshape data based on column values.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame
    index : str or list of str, optional
        Column(s) to use for index
    columns : str or list of str, optional
        Column(s) to use for columns
    values : str or list of str, optional
        Column(s) to use for values

    Returns
    -------
    DataFrame
        Pivoted DataFrame

    Examples
    --------
    >>> df = DataFrame({
    ...     'date': ['2024-01', '2024-01', '2024-02', '2024-02'],
    ...     'type': ['A', 'B', 'A', 'B'],
    ...     'value': [10, 20, 30, 40]
    ... })
    >>> pivoted = df >> pivot(index='date', columns='type', values='value')
    """
    if isinstance(df, DataFrame):
        data = df._data
    else:
        data = df

    result = data.pivot(index=index, columns=columns, values=values)
    return DataFrame(result.reset_index())


def pivot_table(
    df: Union[DataFrame, pd.DataFrame],
    values: Optional[Union[str, List[str]]] = None,
    index: Optional[Union[str, List[str]]] = None,
    columns: Optional[Union[str, List[str]]] = None,
    aggfunc: Union[str, List[str], callable] = "mean",
    fill_value: Optional[Any] = None,
    margins: bool = False,
    dropna: bool = True,
    margins_name: str = "All",
) -> DataFrame:
    """
    Create a pivot table with aggregation.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame
    values : str or list of str, optional
        Column(s) to aggregate
    index : str or list of str, optional
        Column(s) for index
    columns : str or list of str, optional
        Column(s) for columns
    aggfunc : str, list, or callable, default 'mean'
        Aggregation function(s)
    fill_value : scalar, optional
        Value to replace missing values
    margins : bool, default False
        Add row/column margins (subtotals)
    dropna : bool, default True
        Do not include NA values
    margins_name : str, default 'All'
        Name of margin row/column

    Returns
    -------
    DataFrame
        Pivot table

    Examples
    --------
    >>> df = DataFrame({
    ...     'date': ['2024-01', '2024-01', '2024-02', '2024-02'],
    ...     'category': ['A', 'B', 'A', 'B'],
    ...     'sales': [100, 150, 200, 250],
    ...     'units': [10, 15, 20, 25]
    ... })
    >>> table = df >> pivot_table(
    ...     values=['sales', 'units'],
    ...     index='date',
    ...     columns='category',
    ...     aggfunc='sum'
    ... )
    """
    if isinstance(df, DataFrame):
        data = df._data
    else:
        data = df

    result = pd.pivot_table(
        data,
        values=values,
        index=index,
        columns=columns,
        aggfunc=aggfunc,
        fill_value=fill_value,
        margins=margins,
        dropna=dropna,
        margins_name=margins_name,
    )

    return DataFrame(result.reset_index())


# ============================================================================
# Melt and Stack Operations
# ============================================================================


def _melt_impl(
    df: Union[DataFrame, pd.DataFrame],
    id_vars: Optional[Union[str, List[str]]] = None,
    value_vars: Optional[Union[str, List[str]]] = None,
    var_name: str = "variable",
    value_name: str = "value",
    col_level: Optional[Union[int, str]] = None,
    ignore_index: bool = True,
) -> DataFrame:
    """
    Unpivot DataFrame from wide to long format.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame
    id_vars : str or list of str, optional
        Column(s) to use as identifier variables
    value_vars : str or list of str, optional
        Column(s) to unpivot. If None, uses all columns not in id_vars.
    var_name : str, default 'variable'
        Name for variable column
    value_name : str, default 'value'
        Name for value column
    col_level : int or str, optional
        Level to melt if columns are MultiIndex
    ignore_index : bool, default True
        Ignore index

    Returns
    -------
    DataFrame
        Melted DataFrame

    Examples
    --------
    >>> df = DataFrame({
    ...     'id': [1, 2],
    ...     'A': [10, 20],
    ...     'B': [30, 40]
    ... })
    >>> melted = df >> melt(id_vars='id', var_name='letter', value_name='number')
    """
    if isinstance(df, DataFrame):
        data = df._data
    else:
        data = df

    result = pd.melt(
        data,
        id_vars=id_vars,
        value_vars=value_vars,
        var_name=var_name,
        value_name=value_name,
        col_level=col_level,
        ignore_index=ignore_index,
    )

    return DataFrame(result)


def melt(
    id_vars: Optional[Union[str, List[str]]] = None,
    value_vars: Optional[Union[str, List[str]]] = None,
    var_name: str = "variable",
    value_name: str = "value",
    col_level: Optional[Union[int, str]] = None,
    ignore_index: bool = True,
) -> Callable:
    """
    Unpivot DataFrame from wide to long format - curry-friendly wrapper for pipe operator.

    Returns
    -------
    Callable
        Function that takes a DataFrame and applies melt

    Examples
    --------
    >>> df >> melt(id_vars='id', var_name='letter', value_name='number')
    """
    return lambda df: _melt_impl(
        df, id_vars, value_vars, var_name, value_name, col_level, ignore_index
    )


# Alias for tidyr compatibility
gather = melt


def stack(
    df: Union[DataFrame, pd.DataFrame], level: Union[int, str, List] = -1, dropna: bool = True
) -> DataFrame:
    """
    Stack DataFrame columns into rows.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame
    level : int, str, or list, default -1
        Level(s) to stack
    dropna : bool, default True
        Drop rows with missing values

    Returns
    -------
    DataFrame
        Stacked DataFrame

    Examples
    --------
    >>> df = DataFrame({
    ...     'A': [1, 2],
    ...     'B': [3, 4]
    ... })
    >>> stacked = df >> stack()
    """
    if isinstance(df, DataFrame):
        data = df._data
    else:
        data = df

    result = data.stack(level=level, dropna=dropna)
    return DataFrame(result.reset_index())


def unstack(
    df: Union[DataFrame, pd.DataFrame],
    level: Union[int, str, List] = -1,
    fill_value: Optional[Any] = None,
) -> DataFrame:
    """
    Unstack DataFrame rows into columns.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame
    level : int, str, or list, default -1
        Level(s) to unstack
    fill_value : scalar, optional
        Value to use for missing values

    Returns
    -------
    DataFrame
        Unstacked DataFrame

    Examples
    --------
    >>> # Reverse of stack operation
    >>> unstacked = stacked >> unstack()
    """
    if isinstance(df, DataFrame):
        data = df._data
    else:
        data = df

    result = data.unstack(level=level, fill_value=fill_value)
    return DataFrame(result.reset_index())


# Alias for tidyr compatibility
spread = pivot_wider


# ============================================================================
# Column Operations
# ============================================================================


def _separate_impl(
    df: Union[DataFrame, pd.DataFrame],
    col: str,
    into: List[str],
    sep: str = r"\s+",
    remove: bool = True,
    convert: bool = False,
    extra: str = "warn",
    fill: str = "warn",
) -> DataFrame:
    """
    Separate one column into multiple columns (tidyr-style).

    Split a single column into multiple columns based on a separator.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame
    col : str
        Column to separate
    into : list of str
        Names of new columns
    sep : str, default r'\\s+'
        Separator (regex pattern)
    remove : bool, default True
        Remove original column
    convert : bool, default False
        Convert column types
    extra : {'warn', 'drop', 'merge'}, default 'warn'
        How to handle extra values
    fill : {'warn', 'right', 'left'}, default 'warn'
        How to handle missing values

    Returns
    -------
    DataFrame
        DataFrame with separated columns

    Raises
    ------
    PipeFrameColumnError
        If column doesn't exist

    Examples
    --------
    >>> df = DataFrame({
    ...     'name': ['John Doe', 'Jane Smith', 'Bob Jones']
    ... })
    >>> separated = df >> separate('name', into=['first', 'last'], sep=' ')
    >>> print(separated)
    #    first   last
    # 0   John    Doe
    # 1   Jane  Smith
    # 2    Bob  Jones
    """
    if isinstance(df, DataFrame):
        result = df._data.copy()
    else:
        result = df.copy()

    if col not in result.columns:
        raise PipeFrameColumnError(col, list(result.columns))

    # Split the column
    split_data = result[col].str.split(sep, expand=True)

    # Handle extra columns
    if split_data.shape[1] > len(into):
        if extra == "warn":
            import warnings

            warnings.warn(f"More values than expected columns. Using first {len(into)} values.")
            split_data = split_data.iloc[:, : len(into)]
        elif extra == "drop":
            split_data = split_data.iloc[:, : len(into)]
        elif extra == "merge":
            # Merge extra columns into the last column
            for i in range(len(into), split_data.shape[1]):
                split_data.iloc[:, len(into) - 1] = (
                    split_data.iloc[:, len(into) - 1].astype(str)
                    + sep
                    + split_data.iloc[:, i].astype(str)
                )
            split_data = split_data.iloc[:, : len(into)]

    # Handle missing columns
    elif split_data.shape[1] < len(into):
        if fill == "warn":
            import warnings

            warnings.warn(f"Fewer values than expected columns. Filling with None.")
        # Add missing columns
        for i in range(split_data.shape[1], len(into)):
            split_data[i] = None

    # Set column names
    split_data.columns = into

    # Convert types if requested
    if convert:
        split_data = split_data.apply(pd.to_numeric, errors="ignore")

    # Add new columns to result
    for new_col in into:
        result[new_col] = split_data[new_col].values

    # Remove original column if requested
    if remove:
        result = result.drop(columns=[col])

    return DataFrame(result)


def separate(
    col: str,
    into: List[str],
    sep: str = r"\s+",
    remove: bool = True,
    convert: bool = False,
    extra: str = "warn",
    fill: str = "warn",
) -> Callable:
    """
    Separate one column into multiple columns - curry-friendly wrapper for pipe operator.

    Returns
    -------
    Callable
        Function that takes a DataFrame and applies separate

    Examples
    --------
    >>> df >> separate('full_name', into=['first', 'last'], sep=' ')
    """
    return lambda df: _separate_impl(df, col, into, sep, remove, convert, extra, fill)


def _unite_impl(
    df: Union[DataFrame, pd.DataFrame],
    col: str,
    columns: List[str],
    sep: str = "_",
    remove: bool = True,
    na_rm: bool = False,
) -> DataFrame:
    """
    Unite multiple columns into one (tidyr-style).

    Combine multiple columns into a single column with a separator.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame
    col : str
        Name of new united column
    columns : list of str
        Columns to unite
    sep : str, default '_'
        Separator to use
    remove : bool, default True
        Remove original columns
    na_rm : bool, default False
        Remove NA values before uniting

    Returns
    -------
    DataFrame
        DataFrame with united column

    Raises
    ------
    PipeFrameColumnError
        If any specified column doesn't exist

    Examples
    --------
    >>> df = DataFrame({
    ...     'year': [2024, 2024, 2024],
    ...     'month': [1, 2, 3],
    ...     'day': [15, 20, 10]
    ... })
    >>> united = df >> unite('date', ['year', 'month', 'day'], sep='-')
    >>> print(united)
    #          date
    # 0  2024-1-15
    # 1  2024-2-20
    # 2   2024-3-10
    """
    if isinstance(df, DataFrame):
        result = df._data.copy()
    else:
        result = df.copy()

    # Validate columns exist
    for column in columns:
        if column not in result.columns:
            raise PipeFrameColumnError(column, list(result.columns))

    # Unite columns
    if na_rm:
        # Remove NA values before uniting
        result[col] = result[columns].apply(lambda row: sep.join(row.dropna().astype(str)), axis=1)
    else:
        # Include NA values (as string "nan")
        result[col] = result[columns].astype(str).apply(lambda row: sep.join(row), axis=1)

    # Remove original columns if requested
    if remove:
        result = result.drop(columns=columns)

    return DataFrame(result)


def unite(
    col: str,
    columns: List[str],
    sep: str = "_",
    remove: bool = True,
    na_rm: bool = False,
) -> Callable:
    """
    Unite multiple columns into one - curry-friendly wrapper for pipe operator.

    Returns
    -------
    Callable
        Function that takes a DataFrame and applies unite

    Examples
    --------
    >>> df >> unite('date', ['year', 'month', 'day'], sep='-')
    """
    return lambda df: _unite_impl(df, col, columns, sep, remove, na_rm)


# ============================================================================
# Transpose
# ============================================================================


def transpose(df: Union[DataFrame, pd.DataFrame]) -> DataFrame:
    """
    Transpose DataFrame (swap rows and columns).

    Parameters
    ----------
    df : DataFrame
        Input DataFrame

    Returns
    -------
    DataFrame
        Transposed DataFrame

    Examples
    --------
    >>> df = DataFrame({
    ...     'A': [1, 2, 3],
    ...     'B': [4, 5, 6]
    ... })
    >>> transposed = df >> transpose()
    """
    if isinstance(df, DataFrame):
        data = df._data
    else:
        data = df

    return DataFrame(data.T)
