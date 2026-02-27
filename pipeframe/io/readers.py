"""
I/O operations for PipeFrame - read and write data in multiple formats.

This module provides functions to read data from various sources and write
DataFrame objects to different file formats.

Supported formats:
- CSV, TSV
- Excel (xlsx, xls)
- JSON
- Parquet
- Feather
- SQL databases
- Clipboard
- HTML tables
"""

from typing import Any, Dict, List, Optional, Union
import warnings

import pandas as pd

from ..core.dataframe import DataFrame
from ..exceptions import PipeFrameIOError, PipeFrameValueError


# ============================================================================
# CSV/TSV Reading
# ============================================================================


def read_csv(
    filepath_or_buffer: Any,
    sep: str = ",",
    delimiter: Optional[str] = None,
    header: Union[int, List[int], str] = "infer",
    names: Optional[List[str]] = None,
    index_col: Optional[Union[int, str, List]] = None,
    usecols: Optional[Union[List, callable]] = None,
    dtype: Optional[Union[type, Dict]] = None,
    skiprows: Optional[Union[int, List[int], callable]] = None,
    nrows: Optional[int] = None,
    na_values: Optional[Union[str, List, Dict]] = None,
    encoding: Optional[str] = None,
    parse_dates: Union[bool, List, Dict] = False,
    date_parser: Optional[callable] = None,
    **kwargs: Any,
) -> DataFrame:
    """
    Read CSV file into DataFrame.

    Parameters
    ----------
    filepath_or_buffer : str, path object, or file-like object
        Path to CSV file or buffer
    sep : str, default ','
        Delimiter to use
    delimiter : str, optional
        Alternative to sep
    header : int, list of int, or 'infer', default 'infer'
        Row number(s) to use as column names
    names : list, optional
        List of column names to use
    index_col : int, str, or list, optional
        Column(s) to use as row index
    usecols : list or callable, optional
        Columns to use
    dtype : type or dict, optional
        Data type for columns
    skiprows : int, list, or callable, optional
        Rows to skip
    nrows : int, optional
        Number of rows to read
    na_values : str, list, or dict, optional
        Additional strings to recognize as NA
    encoding : str, optional
        Encoding to use
    parse_dates : bool, list, or dict, default False
        Parse date columns
    date_parser : callable, optional
        Function to parse dates
    **kwargs
        Additional arguments passed to pandas.read_csv

    Returns
    -------
    DataFrame
        Data read from CSV file

    Raises
    ------
    PipeFrameIOError
        If file cannot be read

    Examples
    --------
    >>> df = read_csv('data.csv')
    >>> df = read_csv('data.csv', sep=';', encoding='utf-8')
    >>> df = read_csv('data.csv', usecols=['name', 'age'], nrows=1000)
    """
    try:
        result = pd.read_csv(
            filepath_or_buffer,
            sep=sep,
            delimiter=delimiter,
            header=header,
            names=names,
            index_col=index_col,
            usecols=usecols,
            dtype=dtype,
            skiprows=skiprows,
            nrows=nrows,
            na_values=na_values,
            encoding=encoding,
            parse_dates=parse_dates,
            date_parser=date_parser,
            **kwargs,
        )
        return DataFrame(result)
    except Exception as e:
        raise PipeFrameIOError(f"Failed to read CSV file: {str(e)}") from e


def read_tsv(filepath_or_buffer: Any, **kwargs: Any) -> DataFrame:
    """
    Read TSV (tab-separated values) file into DataFrame.

    Convenience wrapper around read_csv with sep='\\t'.

    Parameters
    ----------
    filepath_or_buffer : str, path object, or file-like object
        Path to TSV file or buffer
    **kwargs
        Additional arguments passed to read_csv

    Returns
    -------
    DataFrame
        Data read from TSV file

    Examples
    --------
    >>> df = read_tsv('data.tsv')
    """
    return read_csv(filepath_or_buffer, sep="\t", **kwargs)


# ============================================================================
# Excel Reading
# ============================================================================


def read_excel(
    io: Any,
    sheet_name: Union[str, int, List] = 0,
    header: Union[int, List[int]] = 0,
    names: Optional[List[str]] = None,
    index_col: Optional[Union[int, str, List]] = None,
    usecols: Optional[Union[str, List, callable]] = None,
    dtype: Optional[Union[type, Dict]] = None,
    skiprows: Optional[Union[int, List[int], callable]] = None,
    nrows: Optional[int] = None,
    na_values: Optional[Union[str, List, Dict]] = None,
    parse_dates: Union[bool, List, Dict] = False,
    **kwargs: Any,
) -> Union[DataFrame, Dict[str, DataFrame]]:
    """
    Read Excel file into DataFrame.

    Requires openpyxl (for .xlsx) or xlrd (for .xls).

    Parameters
    ----------
    io : str, path object, or file-like object
        Path to Excel file
    sheet_name : str, int, or list, default 0
        Sheet name or index to read. Use None for all sheets.
    header : int or list of int, default 0
        Row number(s) to use as column names
    names : list, optional
        List of column names to use
    index_col : int, str, or list, optional
        Column(s) to use as row index
    usecols : str, list, or callable, optional
        Columns to use (e.g., 'A:E' or ['A', 'C', 'E'])
    dtype : type or dict, optional
        Data type for columns
    skiprows : int, list, or callable, optional
        Rows to skip
    nrows : int, optional
        Number of rows to read
    na_values : str, list, or dict, optional
        Additional strings to recognize as NA
    parse_dates : bool, list, or dict, default False
        Parse date columns
    **kwargs
        Additional arguments passed to pandas.read_excel

    Returns
    -------
    DataFrame or dict of DataFrames
        Data read from Excel file. If sheet_name is None, returns dict
        with sheet names as keys.

    Raises
    ------
    PipeFrameIOError
        If file cannot be read or required libraries are missing

    Examples
    --------
    >>> df = read_excel('data.xlsx')
    >>> df = read_excel('data.xlsx', sheet_name='Sheet2')
    >>> dfs = read_excel('data.xlsx', sheet_name=None)  # All sheets
    >>> df = read_excel('data.xlsx', usecols='A:E', nrows=100)
    """
    try:
        result = pd.read_excel(
            io,
            sheet_name=sheet_name,
            header=header,
            names=names,
            index_col=index_col,
            usecols=usecols,
            dtype=dtype,
            skiprows=skiprows,
            nrows=nrows,
            na_values=na_values,
            parse_dates=parse_dates,
            **kwargs,
        )

        # Handle multiple sheets
        if isinstance(result, dict):
            return {name: DataFrame(df) for name, df in result.items()}
        return DataFrame(result)

    except ImportError as e:
        raise PipeFrameIOError(
            "Excel support requires openpyxl or xlrd. " "Install with: pip install pipeframe[excel]"
        ) from e
    except Exception as e:
        raise PipeFrameIOError(f"Failed to read Excel file: {str(e)}") from e


# ============================================================================
# JSON Reading
# ============================================================================


def read_json(
    path_or_buf: Any,
    orient: Optional[str] = None,
    typ: str = "frame",
    dtype: Optional[Union[bool, Dict]] = None,
    convert_axes: Optional[bool] = None,
    convert_dates: Union[bool, List[str]] = True,
    keep_default_dates: bool = True,
    precise_float: bool = False,
    date_unit: Optional[str] = None,
    encoding: Optional[str] = None,
    lines: bool = False,
    **kwargs: Any,
) -> DataFrame:
    """
    Read JSON file into DataFrame.

    Parameters
    ----------
    path_or_buf : str, path object, or file-like object
        Path to JSON file or buffer
    orient : str, optional
        Expected JSON string format:
        - 'split' : dict like {index -> [index], columns -> [columns], data -> [values]}
        - 'records' : list like [{column -> value}, ... , {column -> value}]
        - 'index' : dict like {index -> {column -> value}}
        - 'columns' : dict like {column -> {index -> value}}
        - 'values' : just the values array
    typ : {'frame', 'series'}, default 'frame'
        Type of object to return
    dtype : bool or dict, optional
        Data type for columns
    convert_axes : bool, optional
        Try to convert axes to proper dtypes
    convert_dates : bool or list of str, default True
        Parse date columns
    keep_default_dates : bool, default True
        Keep default date columns
    precise_float : bool, default False
        Use higher precision for float values
    date_unit : str, optional
        Timestamp unit to use
    encoding : str, optional
        Encoding to use
    lines : bool, default False
        Read file as JSON lines (one JSON object per line)
    **kwargs
        Additional arguments passed to pandas.read_json

    Returns
    -------
    DataFrame
        Data read from JSON file

    Raises
    ------
    PipeFrameIOError
        If file cannot be read

    Examples
    --------
    >>> df = read_json('data.json')
    >>> df = read_json('data.json', orient='records')
    >>> df = read_json('data.jsonl', lines=True)  # JSON Lines format
    """
    try:
        result = pd.read_json(
            path_or_buf,
            orient=orient,
            typ=typ,
            dtype=dtype,
            convert_axes=convert_axes,
            convert_dates=convert_dates,
            keep_default_dates=keep_default_dates,
            precise_float=precise_float,
            date_unit=date_unit,
            encoding=encoding,
            lines=lines,
            **kwargs,
        )
        return DataFrame(result)
    except Exception as e:
        raise PipeFrameIOError(f"Failed to read JSON file: {str(e)}") from e


# ============================================================================
# Parquet Reading
# ============================================================================


def read_parquet(
    path: Any,
    engine: str = "auto",
    columns: Optional[List[str]] = None,
    use_nullable_dtypes: bool = False,
    **kwargs: Any,
) -> DataFrame:
    """
    Read Parquet file into DataFrame.

    Requires pyarrow or fastparquet.

    Parameters
    ----------
    path : str, path object, or file-like object
        Path to Parquet file
    engine : {'auto', 'pyarrow', 'fastparquet'}, default 'auto'
        Parquet library to use
    columns : list, optional
        Columns to read
    use_nullable_dtypes : bool, default False
        Use nullable dtypes
    **kwargs
        Additional arguments passed to pandas.read_parquet

    Returns
    -------
    DataFrame
        Data read from Parquet file

    Raises
    ------
    PipeFrameIOError
        If file cannot be read or required libraries are missing

    Examples
    --------
    >>> df = read_parquet('data.parquet')
    >>> df = read_parquet('data.parquet', columns=['col1', 'col2'])
    >>> df = read_parquet('data.parquet', engine='pyarrow')
    """
    try:
        result = pd.read_parquet(
            path, engine=engine, columns=columns, use_nullable_dtypes=use_nullable_dtypes, **kwargs
        )
        return DataFrame(result)
    except ImportError as e:
        raise PipeFrameIOError(
            "Parquet support requires pyarrow or fastparquet. "
            "Install with: pip install pipeframe[parquet]"
        ) from e
    except Exception as e:
        raise PipeFrameIOError(f"Failed to read Parquet file: {str(e)}") from e


# ============================================================================
# Feather Reading
# ============================================================================


def read_feather(
    path: Any,
    columns: Optional[List[str]] = None,
    use_threads: bool = True,
    **kwargs: Any,
) -> DataFrame:
    """
    Read Feather file into DataFrame.

    Requires pyarrow.

    Parameters
    ----------
    path : str or path object
        Path to Feather file
    columns : list, optional
        Columns to read
    use_threads : bool, default True
        Use multiple threads for reading
    **kwargs
        Additional arguments passed to pandas.read_feather

    Returns
    -------
    DataFrame
        Data read from Feather file

    Raises
    ------
    PipeFrameIOError
        If file cannot be read or pyarrow is missing

    Examples
    --------
    >>> df = read_feather('data.feather')
    >>> df = read_feather('data.feather', columns=['col1', 'col2'])
    """
    try:
        result = pd.read_feather(path, columns=columns, use_threads=use_threads, **kwargs)
        return DataFrame(result)
    except ImportError as e:
        raise PipeFrameIOError(
            "Feather support requires pyarrow. " "Install with: pip install pyarrow"
        ) from e
    except Exception as e:
        raise PipeFrameIOError(f"Failed to read Feather file: {str(e)}") from e


# ============================================================================
# SQL Reading
# ============================================================================


def read_sql(
    sql: str,
    con: Any,
    index_col: Optional[Union[str, List[str]]] = None,
    coerce_float: bool = True,
    params: Optional[Union[List, Dict]] = None,
    parse_dates: Optional[Union[List, Dict]] = None,
    columns: Optional[List[str]] = None,
    chunksize: Optional[int] = None,
    **kwargs: Any,
) -> DataFrame:
    """
    Read SQL query or table into DataFrame.

    Requires sqlalchemy.

    Parameters
    ----------
    sql : str
        SQL query or table name
    con : SQLAlchemy connectable, str, or sqlite3 connection
        Database connection
    index_col : str or list, optional
        Column(s) to use as row index
    coerce_float : bool, default True
        Convert decimal to float
    params : list or dict, optional
        Parameters to pass to SQL query
    parse_dates : list or dict, optional
        Columns to parse as dates
    columns : list, optional
        Column names to use
    chunksize : int, optional
        Return iterator yielding DataFrames
    **kwargs
        Additional arguments passed to pandas.read_sql

    Returns
    -------
    DataFrame
        Data read from SQL database

    Raises
    ------
    PipeFrameIOError
        If query fails or sqlalchemy is missing

    Examples
    --------
    >>> df = read_sql('SELECT * FROM users', engine)
    >>> df = read_sql('users', engine)  # Read entire table
    >>> df = read_sql('SELECT * FROM users WHERE age > ?', engine, params=[30])
    """
    try:
        result = pd.read_sql(
            sql,
            con,
            index_col=index_col,
            coerce_float=coerce_float,
            params=params,
            parse_dates=parse_dates,
            columns=columns,
            chunksize=chunksize,
            **kwargs,
        )

        if chunksize is not None:
            # Return iterator of DataFrames
            return (DataFrame(chunk) for chunk in result)
        return DataFrame(result)

    except ImportError as e:
        raise PipeFrameIOError(
            "SQL support requires sqlalchemy. " "Install with: pip install pipeframe[sql]"
        ) from e
    except Exception as e:
        raise PipeFrameIOError(f"Failed to read from SQL: {str(e)}") from e


def read_sql_table(
    table_name: str,
    con: Any,
    schema: Optional[str] = None,
    index_col: Optional[Union[str, List[str]]] = None,
    coerce_float: bool = True,
    parse_dates: Optional[Union[List, Dict]] = None,
    columns: Optional[List[str]] = None,
    chunksize: Optional[int] = None,
    **kwargs: Any,
) -> DataFrame:
    """
    Read SQL database table into DataFrame.

    Parameters
    ----------
    table_name : str
        Name of SQL table
    con : SQLAlchemy connectable
        Database connection
    schema : str, optional
        Schema name
    index_col : str or list, optional
        Column(s) to use as row index
    coerce_float : bool, default True
        Convert decimal to float
    parse_dates : list or dict, optional
        Columns to parse as dates
    columns : list, optional
        Column names to use
    chunksize : int, optional
        Return iterator yielding DataFrames
    **kwargs
        Additional arguments

    Returns
    -------
    DataFrame
        Data read from SQL table

    Examples
    --------
    >>> df = read_sql_table('users', engine)
    >>> df = read_sql_table('users', engine, schema='public')
    """
    try:
        result = pd.read_sql_table(
            table_name,
            con,
            schema=schema,
            index_col=index_col,
            coerce_float=coerce_float,
            parse_dates=parse_dates,
            columns=columns,
            chunksize=chunksize,
            **kwargs,
        )

        if chunksize is not None:
            return (DataFrame(chunk) for chunk in result)
        return DataFrame(result)

    except Exception as e:
        raise PipeFrameIOError(f"Failed to read SQL table: {str(e)}") from e


def read_sql_query(
    sql: str,
    con: Any,
    index_col: Optional[Union[str, List[str]]] = None,
    coerce_float: bool = True,
    params: Optional[Union[List, Dict]] = None,
    parse_dates: Optional[Union[List, Dict]] = None,
    chunksize: Optional[int] = None,
    **kwargs: Any,
) -> DataFrame:
    """
    Read SQL query into DataFrame.

    Parameters
    ----------
    sql : str
        SQL query
    con : SQLAlchemy connectable or sqlite3 connection
        Database connection
    index_col : str or list, optional
        Column(s) to use as row index
    coerce_float : bool, default True
        Convert decimal to float
    params : list or dict, optional
        Parameters to pass to query
    parse_dates : list or dict, optional
        Columns to parse as dates
    chunksize : int, optional
        Return iterator yielding DataFrames
    **kwargs
        Additional arguments

    Returns
    -------
    DataFrame
        Data read from SQL query

    Examples
    --------
    >>> df = read_sql_query('SELECT * FROM users WHERE age > 30', engine)
    >>> df = read_sql_query('SELECT * FROM users WHERE city = ?', engine, params=['NYC'])
    """
    try:
        result = pd.read_sql_query(
            sql,
            con,
            index_col=index_col,
            coerce_float=coerce_float,
            params=params,
            parse_dates=parse_dates,
            chunksize=chunksize,
            **kwargs,
        )

        if chunksize is not None:
            return (DataFrame(chunk) for chunk in result)
        return DataFrame(result)

    except Exception as e:
        raise PipeFrameIOError(f"Failed to execute SQL query: {str(e)}") from e


# ============================================================================
# Clipboard Reading
# ============================================================================


def read_clipboard(sep: str = r"\s+", **kwargs: Any) -> DataFrame:
    """
    Read text from clipboard into DataFrame.

    Useful for quickly importing data from spreadsheets.

    Parameters
    ----------
    sep : str, default r'\\s+'
        Delimiter regex
    **kwargs
        Additional arguments passed to read_csv

    Returns
    -------
    DataFrame
        Data read from clipboard

    Raises
    ------
    PipeFrameIOError
        If clipboard cannot be read

    Examples
    --------
    >>> # Copy data from Excel, then:
    >>> df = read_clipboard()
    """
    try:
        result = pd.read_clipboard(sep=sep, **kwargs)
        return DataFrame(result)
    except Exception as e:
        raise PipeFrameIOError(f"Failed to read clipboard: {str(e)}") from e


# ============================================================================
# HTML Reading
# ============================================================================


def read_html(
    io: Any,
    match: str = ".+",
    flavor: Optional[str] = None,
    header: Optional[Union[int, List[int]]] = None,
    index_col: Optional[Union[int, List[int]]] = None,
    skiprows: Optional[Union[int, List[int]]] = None,
    attrs: Optional[Dict[str, str]] = None,
    parse_dates: bool = False,
    thousands: str = ",",
    encoding: Optional[str] = None,
    decimal: str = ".",
    converters: Optional[Dict] = None,
    na_values: Optional[Union[str, List]] = None,
    keep_default_na: bool = True,
    **kwargs: Any,
) -> List[DataFrame]:
    """
    Read HTML tables into list of DataFrames.

    Requires lxml or html5lib.

    Parameters
    ----------
    io : str, path object, or file-like object
        URL, file path, or HTML string
    match : str, default '.+'
        Regex to match table in HTML
    flavor : str, optional
        Parser to use ('lxml', 'html5lib', 'bs4')
    header : int or list of int, optional
        Row number(s) to use as column names
    index_col : int or list of int, optional
        Column(s) to use as row index
    skiprows : int or list of int, optional
        Rows to skip
    attrs : dict, optional
        HTML attributes to match
    parse_dates : bool, default False
        Parse date columns
    thousands : str, default ','
        Thousands separator
    encoding : str, optional
        Encoding to use
    decimal : str, default '.'
        Decimal separator
    converters : dict, optional
        Dict of functions for converting values
    na_values : str or list, optional
        Additional strings to recognize as NA
    keep_default_na : bool, default True
        Keep default NA values
    **kwargs
        Additional arguments

    Returns
    -------
    list of DataFrames
        List of tables found in HTML

    Raises
    ------
    PipeFrameIOError
        If HTML cannot be read or required libraries are missing

    Examples
    --------
    >>> dfs = read_html('https://example.com/table.html')
    >>> df = read_html('data.html')[0]  # First table
    >>> dfs = read_html('page.html', match='Salary', attrs={'id': 'data-table'})
    """
    try:
        result = pd.read_html(
            io,
            match=match,
            flavor=flavor,
            header=header,
            index_col=index_col,
            skiprows=skiprows,
            attrs=attrs,
            parse_dates=parse_dates,
            thousands=thousands,
            encoding=encoding,
            decimal=decimal,
            converters=converters,
            na_values=na_values,
            keep_default_na=keep_default_na,
            **kwargs,
        )
        return [DataFrame(df) for df in result]
    except ImportError as e:
        raise PipeFrameIOError(
            "HTML support requires lxml or html5lib. " "Install with: pip install lxml html5lib"
        ) from e
    except Exception as e:
        raise PipeFrameIOError(f"Failed to read HTML: {str(e)}") from e


# ============================================================================
# Writer Functions
# ============================================================================


def to_csv(
    df: DataFrame, path_or_buf: Optional[Any] = None, sep: str = ",", **kwargs: Any
) -> Optional[str]:
    """
    Write DataFrame to CSV file.

    Parameters
    ----------
    df : DataFrame
        DataFrame to write
    path_or_buf : str, path object, or file-like object, optional
        File path or buffer
    sep : str, default ','
        Delimiter
    **kwargs
        Additional arguments passed to DataFrame.to_csv

    Returns
    -------
    str or None
        CSV string if path_or_buf is None, else None

    Examples
    --------
    >>> to_csv(df, 'output.csv')
    >>> to_csv(df, 'output.csv', index=False)
    >>> csv_string = to_csv(df)
    """
    return df.to_csv(path_or_buf, sep=sep, **kwargs)


def to_excel(df: DataFrame, excel_writer: Any, sheet_name: str = "Sheet1", **kwargs: Any) -> None:
    """
    Write DataFrame to Excel file.

    Parameters
    ----------
    df : DataFrame
        DataFrame to write
    excel_writer : str or ExcelWriter
        File path or ExcelWriter object
    sheet_name : str, default 'Sheet1'
        Sheet name
    **kwargs
        Additional arguments passed to DataFrame.to_excel

    Examples
    --------
    >>> to_excel(df, 'output.xlsx')
    >>> to_excel(df, 'output.xlsx', sheet_name='Data', index=False)
    """
    df.to_excel(excel_writer, sheet_name=sheet_name, **kwargs)


def to_parquet(df: DataFrame, path: str, **kwargs: Any) -> None:
    """
    Write DataFrame to Parquet file.

    Parameters
    ----------
    df : DataFrame
        DataFrame to write
    path : str
        File path
    **kwargs
        Additional arguments passed to DataFrame.to_parquet

    Examples
    --------
    >>> to_parquet(df, 'output.parquet')
    >>> to_parquet(df, 'output.parquet', compression='gzip')
    """
    df.to_parquet(path, **kwargs)


def to_json(df: DataFrame, path_or_buf: Optional[Any] = None, **kwargs: Any) -> Optional[str]:
    """
    Write DataFrame to JSON file.

    Parameters
    ----------
    df : DataFrame
        DataFrame to write
    path_or_buf : str, path object, or file-like object, optional
        File path or buffer
    **kwargs
        Additional arguments passed to DataFrame.to_json

    Returns
    -------
    str or None
        JSON string if path_or_buf is None, else None

    Examples
    --------
    >>> to_json(df, 'output.json')
    >>> to_json(df, 'output.json', orient='records', lines=True)
    >>> json_string = to_json(df, orient='records')
    """
    return df.to_json(path_or_buf, **kwargs)
