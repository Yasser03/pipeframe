"""
Core manipulation verbs for PipeFrame with security hardening.

This module provides all core verb functions for data manipulation including:
- Column operations (define, mutate)
- Row filtering (filter)
- Column selection (select)
- Sorting (arrange)
- Grouping (group_by, summarize)
- Renaming (rename)
- Deduplication (distinct)
- Helper functions (if_else, case_when, selection helpers)

All functions include comprehensive input validation and security hardening.
"""

from typing import Any, Callable, Dict, List, Optional, Union
import pandas as pd
import numpy as np
import re
from functools import partial

from ..core.dataframe import DataFrame
from ..core.series import Series
from ..exceptions import (
    PipeFrameColumnError,
    PipeFrameEmptyDataError,
    PipeFrameExpressionError,
    PipeFrameTypeError,
    PipeFrameValueError,
)


# =============================================================================
# Validation Helpers
# =============================================================================


def _validate_dataframe(df: Any, operation: str) -> None:
    """Validate DataFrame input."""
    if df is None:
        raise PipeFrameValueError(f"Cannot perform '{operation}' on None")
    
    if hasattr(df, 'empty') and df.empty:
        raise PipeFrameEmptyDataError(operation)


def _safe_eval_expression(df: pd.DataFrame, expr: str, column_name: str) -> pd.Series:
    """
    Safely evaluate expression with input validation.
    
    Security: Uses pandas eval() which has limited sandboxing.
    Still validates expression format to prevent obvious attacks.
    """
    # Basic validation
    if not isinstance(expr, str):
        raise PipeFrameTypeError(
            "Expression must be string",
            expected_type=str,
            got_type=type(expr)
        )
    
    # Check for dangerous patterns (basic protection)
    dangerous_patterns = [
        r'__import__',
        r'exec\s*\(',
        r'eval\s*\(',
        r'compile\s*\(',
        r'open\s*\(',
        r'file\s*\(',
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, expr, re.IGNORECASE):
            raise PipeFrameExpressionError(
                expr,
                f"Expression contains potentially dangerous pattern: {pattern}"
            )
    
    
    try:
        import numpy as np
        
        # Check if expression contains module references (pd. or np.)
        # Pandas df.eval() doesn't support module references, so we need to use Python eval for those
        needs_python_eval = 'pd.' in expr or 'np.' in expr
        
        if needs_python_eval:
            # Use Python eval with a restricted safe namespace
            # Create namespace with DataFrame columns and modules
            namespace = {
                'pd': pd,
                'np': np,
                '__builtins__': {},  # Remove built-in functions for safety
            }
            # Add DataFrame columns to namespace
            for col in df.columns:
                namespace[col] = df[col]
            
            result = eval(expr, namespace)
            return result
        else:
            # Use pandas eval for simple DataFrame expressions (safer and faster)
            result = df.eval(expr, level=0)
            return result
    except Exception as e:
        raise PipeFrameExpressionError(
            expr,
            f"Failed to evaluate expression: {str(e)}"
        ) from e


# =============================================================================
# Column Operations
# =============================================================================


def _define_impl(df: Union[DataFrame, pd.DataFrame], **kwargs: Any) -> DataFrame:
    """
    Create or modify columns (SECURITY HARDENED).
    Implementation function - use define() for pipe-friendly version.
    """
    _validate_dataframe(df, 'define')
    
    # Get underlying pandas DataFrame
    if isinstance(df, DataFrame):
        result = df._data.copy()
    else:
        result = df.copy()
    
    for col_name, expr in kwargs.items():
        # Validate column name
        if not isinstance(col_name, str):
            raise PipeFrameTypeError(
                "Column name must be string",
                expected_type=str,
                got_type=type(col_name)
            )
        
        if isinstance(expr, str):
            # Safely evaluate string expression
            result[col_name] = _safe_eval_expression(result, expr, col_name)
        elif callable(expr):
            # Apply callable
            try:
                result[col_name] = expr(DataFrame(result))
            except Exception as e:
                raise PipeFrameExpressionError(
                    f"callable for '{col_name}'",
                    f"Function failed: {str(e)}"
                ) from e
        else:
            # Direct assignment (scalar or array-like)
            result[col_name] = expr
    
    return DataFrame(result)


def define(**kwargs: Any) -> Callable:
    """
    Create or modify columns - curry-friendly wrapper for pipe operator.
    
    Parameters
    ----------
    **kwargs : dict
        Column definitions where keys are column names and values are
        expressions (strings), functions, or constant values
    
    Returns
    -------
    Callable
        Function that takes a DataFrame and applies column definitions
    
    Security
    --------
    String expressions are validated before evaluation. Do not use
    untrusted user input directly in expressions.
    
    Examples
    --------
    >>> df >> define(z='x + y')
    >>> df >> define(ratio='x / y', total='x + y')
    >>> df >> define(category=if_else('value > 0', 'positive', 'negative'))
    """
    return lambda df: _define_impl(df, **kwargs)


# Alias
mutate = define


def _select_impl(df: Union[DataFrame, pd.DataFrame], *args: Any) -> DataFrame:
    """
    Select columns by name or pattern.
    Implementation function - use select() for pipe-friendly version.
    """
    _validate_dataframe(df, 'select')
    
    if isinstance(df, DataFrame):
        data = df._data
    else:
        data = df
    
    all_cols = list(data.columns)
    cols = []
    
    for arg in args:
        if isinstance(arg, str):
            if ':' in arg:
                # Range selection
                start, end = arg.split(':', 1)
                if start not in all_cols:
                    raise PipeFrameColumnError(start, all_cols)
                if end not in all_cols:
                    raise PipeFrameColumnError(end, all_cols)
                
                start_idx = all_cols.index(start)
                end_idx = all_cols.index(end)
                cols.extend(all_cols[start_idx:end_idx + 1])
            else:
                # Single column
                if arg not in all_cols:
                    raise PipeFrameColumnError(arg, all_cols)
                cols.append(arg)
        elif isinstance(arg, list):
            for col in arg:
                if col not in all_cols:
                    raise PipeFrameColumnError(col, all_cols)
            cols.extend(arg)
        elif callable(arg):
            # Function selector
            selected = [col for col in all_cols if arg(col)]
            cols.extend(selected)
        else:
            raise PipeFrameTypeError(
                f"Invalid selector type: {type(arg).__name__}. "
                "Use str, list, or callable"
            )
    
    # Remove duplicates while preserving order
    seen = set()
    unique_cols = []
    for col in cols:
        if col not in seen:
            seen.add(col)
            unique_cols.append(col)
    
    if not unique_cols:
        raise PipeFrameValueError("No columns selected")
    
    return DataFrame(data[unique_cols])


def select(*args: Any) -> Callable:
    """
    Select columns by name or pattern - curry-friendly wrapper for pipe operator.
    
    Parameters
    ----------
    *args : str, list, or callable
        Column specifications
    
    Returns
    -------
    Callable
        Function that takes a DataFrame and applies selection
    
    Examples
    --------
    >>> df >> select('name', 'age')
    >>> df >> select('col1:col5')  # Range
    >>> df >> select(starts_with('date'))
    """
    return lambda df: _select_impl(df, *args)


# =============================================================================
# Row Operations
# =============================================================================


def filter_rows(df: Union[DataFrame, pd.DataFrame], condition: str) -> DataFrame:
    """
    Filter rows based on condition (SECURITY HARDENED).
    
    Parameters
    ----------
    df : DataFrame
        Input data frame
    condition : str
        Boolean expression for filtering
    
    Returns
    -------
    DataFrame
        Filtered data frame
    
    Examples
    --------
    >>> df >> filter_rows('age > 30')
    >>> df >> filter_rows('(age > 30) & (salary > 50000)')
    """
    _validate_dataframe(df, 'filter_rows')
    
    if not isinstance(condition, str):
        raise PipeFrameTypeError(
            "Filter condition must be string expression",
            expected_type=str,
            got_type=type(condition)
        )
    
    if isinstance(df, DataFrame):
        data = df._data
    else:
        data = df
    
    # Validate and evaluate condition
    try:
        result = data.query(condition)
    except Exception as e:
        raise PipeFrameExpressionError(
            condition,
            f"Query failed: {str(e)}"
        ) from e
    
    return DataFrame(result)


def filter(condition: str) -> Callable:
    """
    Filter rows - curry-friendly wrapper for pipe operator.
    
    Parameters
    ----------
    condition : str
        Boolean expression for filtering
    
    Returns
    -------
    Callable
        Function that takes a DataFrame and applies filtering
    
    Examples
    --------
    >>> df >> filter('age > 30')
    >>> df >> filter('(age > 30) & (salary > 50000)')
    """
    return lambda df: filter_rows(df, condition)


def _arrange_impl(df: Union[DataFrame, pd.DataFrame], *columns: Any, **kwargs: Any) -> DataFrame:
    """
    Sort rows by columns.
    Implementation function - use arrange() for pipe-friendly version.
    """
    _validate_dataframe(df, 'arrange')
    
    if not columns:
        raise PipeFrameValueError("Must specify at least one column to sort by")
    
    if isinstance(df, DataFrame):
        data = df._data
    else:
        data = df
    
    na_position = kwargs.get('na_position', 'last')
    
    # Parse column specifications
    sort_cols = []
    sort_ascending = []
    
    for col in columns:
        if isinstance(col, tuple) and col[0] == 'desc':
            # desc() wrapper
            col_name = col[1]
            if col_name not in data.columns:
                raise PipeFrameColumnError(col_name, list(data.columns))
            sort_cols.append(col_name)
            sort_ascending.append(False)
        elif isinstance(col, str):
            if col.startswith('-'):
                # Prefix notation
                col_name = col[1:]
                if col_name not in data.columns:
                    raise PipeFrameColumnError(col_name, list(data.columns))
                sort_cols.append(col_name)
                sort_ascending.append(False)
            else:
                if col not in data.columns:
                    raise PipeFrameColumnError(col, list(data.columns))
                sort_cols.append(col)
                sort_ascending.append(True)
        else:
            raise PipeFrameTypeError(
                f"Invalid sort column type: {type(col).__name__}. "
                "Use str or desc(str)"
            )
    
    result = data.sort_values(
        by=sort_cols,
        ascending=sort_ascending,
        na_position=na_position
    )
    
    return DataFrame(result)


def arrange(*columns: Any, **kwargs: Any) -> Callable:
    """
    Sort rows by columns - curry-friendly wrapper for pipe operator.
    
    Parameters
    ----------
    *columns : str or desc(str)
        Column names to sort by. Prefix with '-' or use desc() for descending
    **kwargs : dict
        ascending, na_position
    
    Returns
    -------
    Callable
        Function that takes a DataFrame and applies sorting
    
    Examples
    --------
    >>> df >> arrange('age')
    >>> df >> arrange('-salary', 'name')
    >>> df >> arrange(desc('score'), 'id')
    """
    return lambda df: _arrange_impl(df, *columns, **kwargs)


def slice_rows(
    df: Union[DataFrame, pd.DataFrame],
    start: int = 0,
    stop: Optional[int] = None,
    step: int = 1
) -> DataFrame:
    """
    Select rows by position.
    
    Parameters
    ----------
    df : DataFrame
        Input data frame
    start : int, default 0
        Starting position
    stop : int, optional
        Ending position
    step : int, default 1
        Step size
    
    Returns
    -------
    DataFrame
        Sliced data frame
    
    Examples
    --------
    >>> df >> slice_rows(0, 10)  # First 10 rows
    >>> df >> slice_rows(step=2)  # Every other row
    """
    _validate_dataframe(df, 'slice_rows')
    
    if isinstance(df, DataFrame):
        data = df._data
    else:
        data = df
    
    if stop is None:
        stop = len(data)
    
    result = data.iloc[start:stop:step]
    return DataFrame(result)


def _distinct_impl(df: Union[DataFrame, pd.DataFrame], *columns: str, **kwargs: Any) -> DataFrame:
    """
    Select distinct/unique rows.
    Implementation function - use distinct() for pipe-friendly version.
    """
    _validate_dataframe(df, 'distinct')
    
    if isinstance(df, DataFrame):
        data = df._data
    else:
        data = df
    
    subset = list(columns) if columns else None
    keep = kwargs.get('keep', 'first')
    
    if subset:
        invalid = [col for col in subset if col not in data.columns]
        if invalid:
            raise PipeFrameColumnError(f"Distinct columns {invalid}", list(data.columns))
    
    result = data.drop_duplicates(subset=subset, keep=keep)
    return DataFrame(result)


def distinct(*columns: str, **kwargs: Any) -> Callable:
    """
    Select distinct/unique rows - curry-friendly wrapper for pipe operator.
    
    Parameters
    ----------
    *columns : str
        Columns to consider for uniqueness (all if none specified)
    **kwargs : dict
        keep: 'first', 'last', or False
    
    Returns
    -------
    Callable
        Function that takes a DataFrame and applies distinct operation
    
    Examples
    --------
    >>> df >> distinct()
    >>> df >> distinct('name', 'city')
    """
    return lambda df: _distinct_impl(df, *columns, **kwargs)


# =============================================================================
# Renaming
# =============================================================================


def _rename_impl(df: Union[DataFrame, pd.DataFrame], **kwargs: Any) -> DataFrame:
    """
    Rename columns.
    Implementation function - use rename() for pipe-friendly version.
    """
    _validate_dataframe(df, 'rename')
    
    if isinstance(df, DataFrame):
        result = df._data.copy()
    else:
        result = df.copy()
    
    # Validate old column names exist
    for new_name, old_name in kwargs.items():
        if old_name not in result.columns:
            raise PipeFrameColumnError(old_name, list(result.columns))
    
    # Reverse the dict for pandas (old->new)
    rename_dict = {v: k for k, v in kwargs.items()}
    result.rename(columns=rename_dict, inplace=True)
    
    return DataFrame(result)


def rename(**kwargs: Any) -> Callable:
    """
    Rename columns - curry-friendly wrapper for pipe operator.
    
    Parameters
    ----------
    **kwargs : dict
        Mapping of new_name=old_name
    
    Returns
    -------
    Callable
        Function that takes a DataFrame and applies renaming
    
    Examples
    --------
    >>> df >> rename(customer_id='cid', customer_name='name')
    """
    return lambda df: _rename_impl(df, **kwargs)


# =============================================================================
# GroupBy Operations
# =============================================================================


def _group_by_impl(df: Union[DataFrame, pd.DataFrame], *columns: str) -> Any:
    """
    Group data frame by columns.
    Implementation function - use group_by() for pipe-friendly version.
    """
    _validate_dataframe(df, 'group_by')
    
    if not columns:
        raise PipeFrameValueError("Must specify at least one column to group by")
    
    if isinstance(df, DataFrame):
        return df.groupby(list(columns))
    else:
        from ..core.dataframe import DataFrame as DF
        return DF(df).groupby(list(columns))


def group_by(*columns: str) -> Callable:
    """
    Group data frame by columns - curry-friendly wrapper for pipe operator.
    
    Parameters
    ----------
    *columns : str
        Column names to group by
    
    Returns
    -------
    Callable
        Function that takes a DataFrame and applies grouping
    
    Examples
    --------
    >>> df >> group_by('dept') >> summarize(avg='mean(salary)')
    """
    return lambda df: _group_by_impl(df, *columns)


def _summarize_impl(grouped_df: Any, **kwargs: Any) -> DataFrame:
    """
    Reduce groups to summaries.
    
    Parameters
    ----------
    grouped_df : GroupBy or DataFrame
        Grouped data frame
    **kwargs : dict
        Summary definitions with aggregation functions
    
    Returns
    -------
    DataFrame
        Summarized data frame
    
    Examples
    --------
    >>> df >> group_by('dept') >> summarize(avg='mean(salary)', count='count()')
    """
    from .groupby import GroupBy
    
    if isinstance(grouped_df, GroupBy):
        # Build aggregation dict
        agg_specs = {}
        
        for col_name, expr in kwargs.items():
            if isinstance(expr, str):
                # Parse expression like 'mean(col)'
                match = re.match(r'(\w+)\((.*?)\)', expr)
                if match:
                    func_name = match.group(1)
                    col = match.group(2).strip()
                    
                    # Special cases
                    if func_name in ['count', 'n', 'size']:
                        # Use size() for count
                        pass  # Handle separately
                    elif col:
                        # Use pandas named aggregation format
                        agg_specs[col_name] = pd.NamedAgg(column=col, aggfunc=func_name)
                    else:
                        # Aggregate all numeric columns
                        agg_specs[col_name] = func_name
                else:
                    raise PipeFrameExpressionError(expr, "Invalid aggregation expression")
        
        # Handle count specially
        count_cols = [k for k, v in kwargs.items() if isinstance(v, str) and 
                     v.split('(')[0] in ['count', 'n', 'size']]
        
        if count_cols:
            # Use size() for count - get underlying pandas DataFrame
            result_df = grouped_df.size().to_frame('count')._data
            if len(count_cols) > 1 or len(agg_specs) > 0:
                # Combine with other aggregations
                if agg_specs:
                    agg_result = grouped_df._grouped.agg(**agg_specs)
                    result_df = result_df.join(agg_result)
            # Rename count column
            if count_cols[0] != 'count':
                result_df = result_df.rename(columns={'count': count_cols[0]})
            return DataFrame(result_df.reset_index())
        
        # Regular aggregations
        if agg_specs:
            result = grouped_df._grouped.agg(**agg_specs)
            return DataFrame(result.reset_index())
        
        return DataFrame(pd.DataFrame())
    
    else:
        # Ungrouped DataFrame - summarize entire frame
        if isinstance(grouped_df, DataFrame):
            data = grouped_df._data
        else:
            data = grouped_df
        
        result_dict = {}
        for col_name, expr in kwargs.items():
            if isinstance(expr, str):
                match = re.match(r'(\w+)\((.*?)\)', expr)
                if match:
                    func_name = match.group(1)
                    col = match.group(2).strip()
                    
                    if func_name in ['count', 'n']:
                        result_dict[col_name] = len(data)
                    elif hasattr(data, func_name):
                        func = getattr(data, func_name)
                        val = func(numeric_only=True)
                        if col and col in val.index:
                            result_dict[col_name] = val[col]
                        else:
                            result_dict[col_name] = val.iloc[0] if len(val) > 0 else None
        
        return DataFrame([result_dict])


def summarize(**kwargs: Any) -> Callable:
    """
    Reduce groups to summaries - curry-friendly wrapper for pipe operator.
    
    Parameters
    ----------
    **kwargs : dict
        Summary definitions with aggregation functions
    
    Returns
    -------
    Callable
        Function that takes a GroupBy or DataFrame and applies summarization
    
    Examples
    --------
    >>> df >> group_by('dept') >> summarize(avg='mean(salary)', count='count()')
    """
    return lambda grouped_df: _summarize_impl(grouped_df, **kwargs)


def ungroup(df: Any) -> DataFrame:
    """
    Remove grouping from GroupBy object.
    
    Parameters
    ----------
    df : DataFrame or GroupBy
        Input data
    
    Returns
    -------
    DataFrame
        Ungrouped DataFrame
    """
    from .groupby import GroupBy
    
    if isinstance(df, GroupBy):
        return df.ungroup()
    elif isinstance(df, DataFrame):
        return df
    else:
        return DataFrame(df)


# =============================================================================
# Conditional Functions
# =============================================================================


def if_else(condition: str, true_value: Any, false_value: Any) -> Callable:
    """
    Vectorized if-else for use in define/mutate.
    
    Parameters
    ----------
    condition : str
        Boolean condition expression
    true_value : Any
        Value if condition is True
    false_value : Any
        Value if condition is False
    
    Returns
    -------
    Callable
        Function that applies the condition
    
    Examples
    --------
    >>> df >> define(status=if_else('value > 0', 'positive', 'negative'))
    """
    def apply_if_else(df: DataFrame) -> pd.Series:
        data = df._data if isinstance(df, DataFrame) else df
        
        try:
            mask = data.eval(condition)
        except Exception as e:
            raise PipeFrameExpressionError(
                condition,
                f"if_else condition failed: {str(e)}"
            ) from e
        
        result = pd.Series(
            np.where(mask, true_value, false_value),
            index=data.index
        )
        return result
    
    return apply_if_else


def case_when(*conditions: tuple, **kwargs: Any) -> Callable:
    """
    Multiple condition if-else (OPTIMIZED).
    
    Parameters
    ----------
    *conditions : tuple
        Pairs of (condition, value)
    **kwargs : dict
        default: default value if no conditions match
    
    Returns
    -------
    Callable
        Function that applies multiple conditions
    
    Examples
    --------
    >>> df >> define(grade=case_when(
    ...     ('score >= 90', 'A'),
    ...     ('score >= 80', 'B'),
    ...     ('score >= 70', 'C'),
    ...     default='F'
    ... ))
    """
    default_value = kwargs.get('default', None)
    
    def apply_case_when(df: DataFrame) -> pd.Series:
        data = df._data if isinstance(df, DataFrame) else df
        
        # Use vectorized np.select for performance
        conditions_list = []
        choices_list = []
        
        for condition, value in conditions:
            try:
                mask = data.eval(condition)
                conditions_list.append(mask)
                choices_list.append(value)
            except Exception as e:
                raise PipeFrameExpressionError(
                    condition,
                    f"case_when condition failed: {str(e)}"
                ) from e
        
        result = pd.Series(
            np.select(conditions_list, choices_list, default=default_value),
            index=data.index
        )
        return result
    
    return apply_case_when


# =============================================================================
# Selection Helpers
# =============================================================================


def starts_with(prefix: str) -> Callable:
    """Select columns that start with a prefix."""
    return lambda col: str(col).startswith(prefix)


def ends_with(suffix: str) -> Callable:
    """Select columns that end with a suffix."""
    return lambda col: str(col).endswith(suffix)


def contains(substring: str) -> Callable:
    """Select columns that contain a substring."""
    return lambda col: substring in str(col)


def matches(pattern: str) -> Callable:
    """Select columns that match a regex pattern."""
    compiled = re.compile(pattern)
    return lambda col: compiled.match(str(col)) is not None


def one_of(*cols: str) -> Callable:
    """Select columns that are in the list."""
    cols_set = set(cols)
    return lambda col: col in cols_set


def desc(col: str) -> tuple:
    """Helper for descending order in arrange."""
    return ('desc', col)
