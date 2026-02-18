"""
Utility functions and decorators for PipeFrame.

This module provides helpful utilities that make working with PipeFrame
even more convenient.
"""

from typing import Any, Callable, Dict, List, Optional, Union
from functools import wraps
import time
import warnings

import pandas as pd

from ..core.dataframe import DataFrame


# ============================================================================
# Decorators
# ============================================================================


def timer(func: Callable) -> Callable:
    """
    Decorator to time function execution.
    
    Useful for profiling data pipelines.
    
    Examples
    --------
    >>> @timer
    ... def slow_function(df):
    ...     return df >> filter('x > 100') >> group_by('category')
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"⏱️  {func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper


def catch_empty(default: Any = None) -> Callable:
    """
    Decorator to handle empty DataFrames gracefully.
    
    Parameters
    ----------
    default : Any, optional
        Value to return if DataFrame is empty
    
    Examples
    --------
    >>> @catch_empty(default=DataFrame())
    ... def process(df):
    ...     return df >> filter('x > 1000')  # Might return empty
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            if isinstance(result, DataFrame) and result.empty:
                warnings.warn(f"{func.__name__} returned empty DataFrame")
                return default
            return result
        return wrapper
    return decorator


def validate_columns(*required_cols: str) -> Callable:
    """
    Decorator to validate DataFrame has required columns.
    
    Parameters
    ----------
    *required_cols : str
        Column names that must be present
    
    Raises
    ------
    ValueError
        If any required columns are missing
    
    Examples
    --------
    >>> @validate_columns('name', 'age', 'salary')
    ... def process_employees(df):
    ...     return df >> filter('age > 30')
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(df: Union[DataFrame, pd.DataFrame], *args: Any, **kwargs: Any) -> Any:
            data = df._data if isinstance(df, DataFrame) else df
            missing = [col for col in required_cols if col not in data.columns]
            if missing:
                raise ValueError(
                    f"{func.__name__} requires columns: {required_cols}. "
                    f"Missing: {missing}"
                )
            return func(df, *args, **kwargs)
        return wrapper
    return decorator


# ============================================================================
# Snapshot and Compare
# ============================================================================


class Snapshot:
    """
    Take snapshots of DataFrames for comparison.
    
    Useful for debugging pipelines and tracking changes.
    
    Examples
    --------
    >>> snap = Snapshot()
    >>> 
    >>> result = (df
    ...     >> snap.capture('after_filter')
    ...     >> filter('x > 50')
    ...     >> snap.capture('after_group')
    ...     >> group_by('category')
    ... )
    >>> 
    >>> snap.compare('after_filter', 'after_group')
    """
    
    def __init__(self):
        """Initialize snapshot tracker."""
        self._snapshots: Dict[str, DataFrame] = {}
    
    def capture(self, name: str) -> Callable:
        """
        Create a capture function for use in pipes.
        
        Parameters
        ----------
        name : str
            Name for this snapshot
        
        Returns
        -------
        Callable
            Function that can be used in pipe
        """
        def _capture(df: Union[DataFrame, pd.DataFrame]) -> DataFrame:
            result = DataFrame(df) if not isinstance(df, DataFrame) else df
            self._snapshots[name] = result.copy()
            return result
        return _capture
    
    def get(self, name: str) -> Optional[DataFrame]:
        """Get a snapshot by name."""
        return self._snapshots.get(name)
    
    def list(self) -> List[str]:
        """List all snapshot names."""
        return list(self._snapshots.keys())
    
    def compare(self, name1: str, name2: str) -> Dict[str, Any]:
        """
        Compare two snapshots.
        
        Returns
        -------
        dict
            Comparison statistics
        """
        if name1 not in self._snapshots:
            raise ValueError(f"Snapshot '{name1}' not found")
        if name2 not in self._snapshots:
            raise ValueError(f"Snapshot '{name2}' not found")
        
        df1 = self._snapshots[name1]
        df2 = self._snapshots[name2]
        
        return {
            'rows_before': len(df1),
            'rows_after': len(df2),
            'rows_changed': len(df2) - len(df1),
            'cols_before': len(df1.columns),
            'cols_after': len(df2.columns),
            'cols_added': list(set(df2.columns) - set(df1.columns)),
            'cols_removed': list(set(df1.columns) - set(df2.columns)),
        }
    
    def clear(self):
        """Clear all snapshots."""
        self._snapshots.clear()


# ============================================================================
# Quick Profiling
# ============================================================================


def profile_pipeline(df: DataFrame, *operations: Callable, verbose: bool = True) -> DataFrame:
    """
    Profile a series of operations to identify bottlenecks.
    
    Parameters
    ----------
    df : DataFrame
        Input DataFrame
    *operations : Callable
        Operations to profile
    verbose : bool, default True
        Print timing information
    
    Returns
    -------
    DataFrame
        Final result after all operations
    
    Examples
    --------
    >>> from pipeframe import filter, group_by, summarize
    >>> 
    >>> result = profile_pipeline(
    ...     df,
    ...     filter('age > 30'),
    ...     group_by('dept'),
    ...     summarize(avg='mean(salary)')
    ... )
    """
    result = df
    total_time = 0
    
    for i, op in enumerate(operations, 1):
        start = time.time()
        result = result >> op
        elapsed = time.time() - start
        total_time += elapsed
        
        if verbose:
            op_name = getattr(op, '__name__', f'operation_{i}')
            print(f"  Step {i} ({op_name}): {elapsed:.3f}s")
    
    if verbose:
        print(f"  Total: {total_time:.3f}s")
    
    return result


# ============================================================================
# Data Validation
# ============================================================================


def check_data_quality(df: DataFrame, checks: Optional[Dict[str, Callable]] = None) -> Dict[str, bool]:
    """
    Run data quality checks on DataFrame.
    
    Parameters
    ----------
    df : DataFrame
        DataFrame to check
    checks : dict, optional
        Custom checks as {name: check_function}
    
    Returns
    -------
    dict
        Results of each check
    
    Examples
    --------
    >>> checks = {
    ...     'no_nulls': lambda df: df.isnull().sum().sum() == 0,
    ...     'positive_salary': lambda df: (df['salary'] > 0).all(),
    ...     'valid_ages': lambda df: df['age'].between(18, 100).all()
    ... }
    >>> 
    >>> results = check_data_quality(df, checks)
    """
    default_checks = {
        'not_empty': lambda d: len(d) > 0,
        'no_duplicate_columns': lambda d: len(d.columns) == len(set(d.columns)),
    }
    
    all_checks = {**default_checks, **(checks or {})}
    data = df._data if isinstance(df, DataFrame) else df
    
    results = {}
    for name, check in all_checks.items():
        try:
            results[name] = bool(check(data))
        except Exception as e:
            results[name] = False
            warnings.warn(f"Check '{name}' failed: {e}")
    
    return results


# ============================================================================
# Sample and Debug
# ============================================================================


def _peek_impl(df: DataFrame, n: int = 5, where: str = 'head', message: Optional[str] = None) -> DataFrame:
    """
    Quick peek at data (useful in pipes for debugging).
    
    Parameters
    ----------
    df : DataFrame
        Input DataFrame
    n : int, default 5
        Number of rows to show
    where : {'head', 'tail', 'sample'}, default 'head'
        Which rows to show
    
    Returns
    -------
    DataFrame
        Original DataFrame (unchanged)
    
    Examples
    --------
    >>> result = (df
    ...     >> filter('x > 50')
    ...     >> peek(3)  # Quick look at intermediate result
    ...     >> group_by('category')
    ... )
    """
    data = df._data if isinstance(df, DataFrame) else df
    
    print(f"\n{'='*60}")
    if message:
        print(message)
    print(f"Peek ({where}, n={n}): {len(data)} rows × {len(data.columns)} cols")
    print(f"{'='*60}")
    
    if where == 'head':
        print(data.head(n))
    elif where == 'tail':
        print(data.tail(n))
    elif where == 'sample':
        print(data.sample(min(n, len(data))))
    
    print(f"{'='*60}\n")
    
    return df


def peek(arg: Any = 5, n: int = 5, where: str = 'head') -> Callable:
    """
    Quick peek at data - curry-friendly wrapper for pipe operator.
    
    Parameters
    ----------
    arg : Any, optional
        Either the message string to display or the number of rows (n)
    n : int, default 5
        Number of rows to show (if arg is used for message)
    where : {'head', 'tail', 'sample'}, default 'head'
        Which rows to show
    
    Returns
    -------
    Callable
        Function that takes a DataFrame and displays it
    
    Examples
    --------
    >>> result = df >> peek("Checking progress") >> define(x='y * 2')
    >>> result = df >> peek(3) >> define(x='y * 2')
    """
    message = None
    if isinstance(arg, str):
        message = arg
    elif isinstance(arg, int):
        n = arg
        
    return lambda df: _peek_impl(df, n, where, message)


def describe_pipeline(df: DataFrame, *operations: Callable) -> None:
    """
    Describe what a pipeline will do without executing it.
    
    Parameters
    ----------
    df : DataFrame
        Input DataFrame
    *operations : Callable
        Operations to describe
    
    Examples
    --------
    >>> describe_pipeline(
    ...     df,
    ...     filter('age > 30'),
    ...     group_by('dept'),
    ...     summarize(avg='mean(salary)')
    ... )
    """
    print(f"\n📊 Pipeline Description")
    print(f"{'='*60}")
    print(f"Input: {len(df)} rows × {len(df.columns)} columns")
    print(f"\nOperations:")
    
    for i, op in enumerate(operations, 1):
        op_name = getattr(op, '__name__', 'operation')
        print(f"  {i}. {op_name}")
    
    print(f"{'='*60}\n")
