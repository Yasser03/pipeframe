"""
Enhanced PipeFrame DataFrame implementation with security and error handling.

This module provides a production-ready DataFrame class with:
- Comprehensive input validation
- Security-hardened expression evaluation
- Proper error messages
- Full type hints
- Performance optimizations
"""

from typing import Any, Callable, Dict, List, Optional, Union

import numpy as np
import pandas as pd

from .index import Index
from .series import Series
from ..exceptions import (
    PipeFrameColumnError,
    PipeFrameEmptyDataError,
    PipeFrameExpressionError,
    PipeFrameTypeError,
    PipeFrameValueError,
)


class DataFrame:
    """
    PipeFrame DataFrame - A grammar-based data structure for manipulation.

    Wraps pandas DataFrame and adds a pipe-based grammar for intuitive
    data manipulation workflows.

    Parameters
    ----------
    data : ndarray, Iterable, dict, DataFrame, or pd.DataFrame, optional
        Data to initialize DataFrame
    index : Index or array-like, optional
        Index to use for resulting frame
    columns : Index or array-like, optional
        Column labels to use
    dtype : dtype, optional
        Data type to force
    copy : bool, default False
        Copy data from inputs

    Examples
    --------
    >>> df = DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    >>> result = df >> filter('x > 1') >> define(z='x + y')

    Security Notes
    --------------
    String expressions are evaluated using pandas' eval() which provides
    some sandboxing, but you should still only use expressions from
    trusted sources.
    """

    def __init__(
        self,
        data: Optional[Any] = None,
        index: Optional[Any] = None,
        columns: Optional[Any] = None,
        dtype: Optional[Any] = None,
        copy: bool = False,
    ):
        """Initialize a PipeFrame DataFrame."""
        if isinstance(data, pd.DataFrame):
            self._data = data.copy() if copy else data
        elif isinstance(data, DataFrame):
            self._data = data._data.copy() if copy else data._data
        else:
            self._data = pd.DataFrame(data, index=index, columns=columns, dtype=dtype, copy=copy)

    # ======================================================================
    # Magic Methods
    # ======================================================================

    def __rshift__(self, other: Callable) -> "DataFrame":
        """
        Pipe operator for verb chaining with enhanced error handling.

        Parameters
        ----------
        other : callable
            Function to apply to this DataFrame

        Returns
        -------
        DataFrame
            Result of applying the function

        Raises
        ------
        PipeFrameTypeError
            If other is not callable
        RuntimeError
            If the pipe operation fails

        Examples
        --------
        >>> df >> filter('x > 1') >> define(z='x + y')
        """
        if not callable(other):
            raise PipeFrameTypeError(
                f"Pipe operator '>>' requires callable, got {type(other).__name__}"
            )

        try:
            result = other(self)
        except Exception as e:
            raise RuntimeError(f"Pipe operation failed: {str(e)}") from e

        # Ensure we return a DataFrame or GroupBy
        if isinstance(result, DataFrame):
            return result
        elif isinstance(result, pd.DataFrame):
            return DataFrame(result)
        else:
            # Check if it's a GroupBy object (avoid circular import)
            if type(result).__name__ == 'GroupBy':
                return result
            raise PipeFrameTypeError(
                f"Pipe function must return DataFrame or GroupBy, got {type(result).__name__}"
            )

    def __getitem__(self, key: Union[str, List[str], slice]) -> Union["DataFrame", Series]:
        """
        Get item with enhanced error handling.

        Parameters
        ----------
        key : str, list of str, or slice
            Column name(s) or slice

        Returns
        -------
        DataFrame or Series
            Selected columns

        Raises
        ------
        PipeFrameColumnError
            If column doesn't exist
        """
        if isinstance(key, str):
            if key not in self._data.columns:
                raise PipeFrameColumnError(key, list(self._data.columns))
            return Series(self._data[key])
        elif isinstance(key, list):
            invalid = [col for col in key if col not in self._data.columns]
            if invalid:
                raise PipeFrameColumnError(
                    f"Columns {invalid}", list(self._data.columns)
                )
            return DataFrame(self._data[key])
        else:
            return DataFrame(self._data[key])

    def __setitem__(self, key: str, value: Any) -> None:
        """Column assignment with validation."""
        if not isinstance(key, str):
            raise PipeFrameTypeError("Column name must be string", expected_type=str, got_type=type(key))
        self._data[key] = value

    def __len__(self) -> int:
        """Return number of rows."""
        return len(self._data)

    def __repr__(self) -> str:
        """String representation."""
        return f"<pipeframe.DataFrame shape={self.shape}>\n{self._data.__repr__()}"

    def __str__(self) -> str:
        """String representation for printing."""
        return self._data.__str__()

    def __iter__(self):
        """Iterate over column names."""
        return iter(self._data)

    # ======================================================================
    # Properties
    # ======================================================================

    @property
    def shape(self) -> tuple:
        """Return shape (rows, columns)."""
        return self._data.shape

    @property
    def columns(self) -> Index:
        """Return column labels."""
        return Index(self._data.columns)

    @columns.setter
    def columns(self, value: Any) -> None:
        """Set column labels."""
        self._data.columns = value

    @property
    def index(self) -> Index:
        """Return row index."""
        return Index(self._data.index)

    @index.setter
    def index(self, value: Any) -> None:
        """Set row index."""
        self._data.index = value

    @property
    def dtypes(self) -> Series:
        """Return data types."""
        return Series(self._data.dtypes)

    @property
    def values(self) -> np.ndarray:
        """Return numpy array representation."""
        return self._data.values

    @property
    def T(self) -> "DataFrame":
        """Transpose DataFrame."""
        return DataFrame(self._data.T)

    @property
    def empty(self) -> bool:
        """Return True if DataFrame is empty."""
        return self._data.empty

    @property
    def size(self) -> int:
        """Return total number of elements."""
        return self._data.size

    @property
    def iloc(self) -> Any:
        """Integer-location based indexing."""
        return self._data.iloc

    @property
    def loc(self) -> Any:
        """Label-based indexing."""
        return self._data.loc

    # ======================================================================
    # Conversion Methods
    # ======================================================================

    def to_pandas(self) -> pd.DataFrame:
        """Convert to pandas DataFrame."""
        return self._data.copy()

    @classmethod
    def from_pandas(cls, df: pd.DataFrame, copy: bool = False) -> "DataFrame":
        """
        Create PipeFrame DataFrame from pandas DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Pandas DataFrame to convert
        copy : bool, default False
            Whether to copy the data

        Returns
        -------
        DataFrame
            PipeFrame DataFrame
        """
        return cls(df, copy=copy)

    def to_numpy(self) -> np.ndarray:
        """Convert to numpy array."""
        return self._data.to_numpy()

    def to_dict(self, orient: str = "dict", into: type = dict) -> Union[Dict, List]:
        """
        Convert to dictionary.

        Parameters
        ----------
        orient : str, default 'dict'
            Type of dict to convert to: 'dict', 'list', 'series', 'split',
            'records', 'index'
        into : type, default dict
            Type to return

        Returns
        -------
        dict or list
            Converted dictionary
        """
        return self._data.to_dict(orient=orient, into=into)

    def copy(self, deep: bool = True) -> "DataFrame":
        """
        Create a copy of this DataFrame.

        Parameters
        ----------
        deep : bool, default True
            Make a deep copy, including a copy of the data

        Returns
        -------
        DataFrame
            Copy of calling DataFrame
        """
        return DataFrame(self._data.copy(deep=deep))

    # ======================================================================
    # Information Methods
    # ======================================================================

    def info(
        self,
        verbose: Optional[bool] = None,
        buf: Optional[Any] = None,
        max_cols: Optional[int] = None,
        memory_usage: Optional[Union[bool, str]] = None,
        show_counts: Optional[bool] = None,
    ) -> None:
        """
        Print DataFrame information.

        Parameters
        ----------
        verbose : bool, optional
            Whether to print full summary
        buf : writable buffer, optional
            Where to send output
        max_cols : int, optional
            Max columns to print
        memory_usage : bool or str, optional
            Whether to display memory usage
        show_counts : bool, optional
            Whether to show non-null counts
        """
        self._data.info(
            verbose=verbose,
            buf=buf,
            max_cols=max_cols,
            memory_usage=memory_usage,
            show_counts=show_counts,
        )

    def describe(
        self,
        percentiles: Optional[List[float]] = None,
        include: Optional[Union[str, List[type]]] = None,
        exclude: Optional[Union[str, List[type]]] = None,
    ) -> "DataFrame":
        """
        Generate descriptive statistics.

        Parameters
        ----------
        percentiles : list of float, optional
            Percentiles to include (default: [.25, .5, .75])
        include : 'all', list of dtypes, optional
            Data types to include
        exclude : list of dtypes, optional
            Data types to exclude

        Returns
        -------
        DataFrame
            Summary statistics
        """
        return DataFrame(
            self._data.describe(percentiles=percentiles, include=include, exclude=exclude)
        )

    def head(self, n: int = 5) -> "DataFrame":
        """
        Return first n rows.

        Parameters
        ----------
        n : int, default 5
            Number of rows to return

        Returns
        -------
        DataFrame
            First n rows
        """
        return DataFrame(self._data.head(n))

    def tail(self, n: int = 5) -> "DataFrame":
        """
        Return last n rows.

        Parameters
        ----------
        n : int, default 5
            Number of rows to return

        Returns
        -------
        DataFrame
            Last n rows
        """
        return DataFrame(self._data.tail(n))

    def sample(
        self,
        n: Optional[int] = None,
        frac: Optional[float] = None,
        replace: bool = False,
        weights: Optional[Union[str, np.ndarray]] = None,
        random_state: Optional[Union[int, np.random.RandomState]] = None,
        axis: Optional[int] = None,
        ignore_index: bool = False,
    ) -> "DataFrame":
        """
        Return a random sample of items.

        Parameters
        ----------
        n : int, optional
            Number of items to return
        frac : float, optional
            Fraction of items to return
        replace : bool, default False
            Sample with or without replacement
        weights : str or ndarray, optional
            Weights for sampling
        random_state : int or RandomState, optional
            Random number generator seed
        axis : int, optional
            Axis to sample (0 or 1)
        ignore_index : bool, default False
            Do not use index values along the row axis

        Returns
        -------
        DataFrame
            Random sample
        """
        return DataFrame(
            self._data.sample(
                n=n,
                frac=frac,
                replace=replace,
                weights=weights,
                random_state=random_state,
                axis=axis,
                ignore_index=ignore_index,
            )
        )

    def memory_usage(self, index: bool = True, deep: bool = False) -> Series:
        """
        Return memory usage of each column.

        Parameters
        ----------
        index : bool, default True
            Include memory usage of the index
        deep : bool, default False
            Introspect data deeply

        Returns
        -------
        Series
            Memory usage in bytes
        """
        return Series(self._data.memory_usage(index=index, deep=deep))

    # ======================================================================
    # Missing Data Methods
    # ======================================================================

    def isna(self) -> "DataFrame":
        """Detect missing values."""
        return DataFrame(self._data.isna())

    def isnull(self) -> "DataFrame":
        """Detect missing values (alias for isna)."""
        return self.isna()

    def notna(self) -> "DataFrame":
        """Detect non-missing values."""
        return DataFrame(self._data.notna())

    def notnull(self) -> "DataFrame":
        """Detect non-missing values (alias for notna)."""
        return self.notna()

    def dropna(
        self,
        axis: int = 0,
        how: str = "any",
        thresh: Optional[int] = None,
        subset: Optional[List[str]] = None,
        inplace: bool = False,
    ) -> Optional["DataFrame"]:
        """
        Remove missing values.

        Parameters
        ----------
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Determine if rows or columns are removed
        how : {'any', 'all'}, default 'any'
            Require that many non-NA values
        thresh : int, optional
            Require that many non-NA values
        subset : list of str, optional
            Labels to consider
        inplace : bool, default False
            Modify in place

        Returns
        -------
        DataFrame or None
            DataFrame with NA entries dropped or None if inplace=True
        """
        if subset:
            invalid = [col for col in subset if col not in self._data.columns]
            if invalid:
                raise PipeFrameColumnError(f"Subset columns {invalid}", list(self._data.columns))

        if inplace:
            self._data.dropna(axis=axis, how=how, thresh=thresh, subset=subset, inplace=True)
            return None
        return DataFrame(self._data.dropna(axis=axis, how=how, thresh=thresh, subset=subset))

    def fillna(
        self,
        value: Optional[Any] = None,
        method: Optional[str] = None,
        axis: Optional[int] = None,
        inplace: bool = False,
        limit: Optional[int] = None,
        downcast: Optional[Dict] = None,
    ) -> Optional["DataFrame"]:
        """
        Fill missing values.

        Parameters
        ----------
        value : scalar, dict, Series, or DataFrame, optional
            Value to use to fill holes
        method : {'backfill', 'bfill', 'pad', 'ffill', None}, default None
            Method to use for filling holes
        axis : {0 or 'index', 1 or 'columns'}, optional
            Axis along which to fill
        inplace : bool, default False
            Modify in place
        limit : int, optional
            Maximum number of consecutive NaN values to forward/backward fill
        downcast : dict, optional
            Dict of item->dtype to downcast

        Returns
        -------
        DataFrame or None
            DataFrame with NA entries filled or None if inplace=True
        """
        if inplace:
            self._data.fillna(
                value=value,
                method=method,
                axis=axis,
                limit=limit,
                downcast=downcast,
                inplace=True,
            )
            return None
        return DataFrame(
            self._data.fillna(
                value=value, method=method, axis=axis, limit=limit, downcast=downcast
            )
        )

    def interpolate(
        self,
        method: str = "linear",
        axis: int = 0,
        limit: Optional[int] = None,
        inplace: bool = False,
        **kwargs: Any,
    ) -> Optional["DataFrame"]:
        """
        Interpolate missing values.

        Parameters
        ----------
        method : str, default 'linear'
            Interpolation technique
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Interpolation axis
        limit : int, optional
            Maximum number of consecutive NaNs to fill
        inplace : bool, default False
            Update the data in place
        **kwargs
            Additional arguments passed to interpolation function

        Returns
        -------
        DataFrame or None
            Interpolated DataFrame or None if inplace=True
        """
        if inplace:
            self._data.interpolate(method=method, axis=axis, limit=limit, **kwargs, inplace=True)
            return None
        return DataFrame(self._data.interpolate(method=method, axis=axis, limit=limit, **kwargs))

    # ======================================================================
    # Aggregation Methods
    # ======================================================================

    def sum(
        self, axis: Optional[int] = None, skipna: bool = True, numeric_only: bool = False, **kwargs: Any
    ) -> Union[Series, Any]:
        """Return sum of values."""
        result = self._data.sum(axis=axis, skipna=skipna, numeric_only=numeric_only, **kwargs)
        if isinstance(result, pd.Series):
            return Series(result)
        return result

    def mean(
        self, axis: Optional[int] = None, skipna: bool = True, numeric_only: bool = False, **kwargs: Any
    ) -> Union[Series, Any]:
        """Return mean of values."""
        result = self._data.mean(axis=axis, skipna=skipna, numeric_only=numeric_only, **kwargs)
        if isinstance(result, pd.Series):
            return Series(result)
        return result

    def median(
        self, axis: Optional[int] = None, skipna: bool = True, numeric_only: bool = False, **kwargs: Any
    ) -> Union[Series, Any]:
        """Return median of values."""
        result = self._data.median(axis=axis, skipna=skipna, numeric_only=numeric_only, **kwargs)
        if isinstance(result, pd.Series):
            return Series(result)
        return result

    def min(
        self, axis: Optional[int] = None, skipna: bool = True, numeric_only: bool = False, **kwargs: Any
    ) -> Union[Series, Any]:
        """Return minimum value."""
        result = self._data.min(axis=axis, skipna=skipna, numeric_only=numeric_only, **kwargs)
        if isinstance(result, pd.Series):
            return Series(result)
        return result

    def max(
        self, axis: Optional[int] = None, skipna: bool = True, numeric_only: bool = False, **kwargs: Any
    ) -> Union[Series, Any]:
        """Return maximum value."""
        result = self._data.max(axis=axis, skipna=skipna, numeric_only=numeric_only, **kwargs)
        if isinstance(result, pd.Series):
            return Series(result)
        return result

    def std(
        self,
        axis: Optional[int] = None,
        skipna: bool = True,
        ddof: int = 1,
        numeric_only: bool = False,
        **kwargs: Any,
    ) -> Union[Series, Any]:
        """Return standard deviation."""
        result = self._data.std(
            axis=axis, skipna=skipna, ddof=ddof, numeric_only=numeric_only, **kwargs
        )
        if isinstance(result, pd.Series):
            return Series(result)
        return result

    def var(
        self,
        axis: Optional[int] = None,
        skipna: bool = True,
        ddof: int = 1,
        numeric_only: bool = False,
        **kwargs: Any,
    ) -> Union[Series, Any]:
        """Return variance."""
        result = self._data.var(
            axis=axis, skipna=skipna, ddof=ddof, numeric_only=numeric_only, **kwargs
        )
        if isinstance(result, pd.Series):
            return Series(result)
        return result

    def count(self, axis: int = 0, numeric_only: bool = False) -> Series:
        """Count non-NA cells."""
        result = self._data.count(axis=axis, numeric_only=numeric_only)
        return Series(result)

    def nunique(self, axis: int = 0, dropna: bool = True) -> Series:
        """Count distinct observations."""
        result = self._data.nunique(axis=axis, dropna=dropna)
        return Series(result)

    def quantile(
        self,
        q: Union[float, List[float]] = 0.5,
        axis: int = 0,
        numeric_only: bool = True,
        interpolation: str = "linear",
    ) -> Union["DataFrame", Series]:
        """Return values at the given quantile."""
        result = self._data.quantile(q=q, axis=axis, numeric_only=numeric_only, interpolation=interpolation)
        if isinstance(result, pd.DataFrame):
            return DataFrame(result)
        return Series(result)

    # ======================================================================
    # Merging and Joining
    # ======================================================================

    def merge(
        self,
        right: Union["DataFrame", pd.DataFrame],
        how: str = "inner",
        on: Optional[Union[str, List[str]]] = None,
        left_on: Optional[Union[str, List[str]]] = None,
        right_on: Optional[Union[str, List[str]]] = None,
        left_index: bool = False,
        right_index: bool = False,
        suffixes: tuple = ("_x", "_y"),
        validate: Optional[str] = None,
    ) -> "DataFrame":
        """
        Merge with another DataFrame.

        Parameters
        ----------
        right : DataFrame
            DataFrame to merge with
        how : {'left', 'right', 'outer', 'inner', 'cross'}, default 'inner'
            Type of merge
        on : str or list of str, optional
            Column names to join on
        left_on : str or list of str, optional
            Left DataFrame columns to join on
        right_on : str or list of str, optional
            Right DataFrame columns to join on
        left_index : bool, default False
            Use index from left DataFrame as join key
        right_index : bool, default False
            Use index from right DataFrame as join key
        suffixes : 2-tuple, default ('_x', '_y')
            Suffixes to apply to overlapping column names
        validate : str, optional
            Validation type

        Returns
        -------
        DataFrame
            Merged DataFrame
        """
        right_df = right._data if isinstance(right, DataFrame) else right
        result = self._data.merge(
            right_df,
            how=how,
            on=on,
            left_on=left_on,
            right_on=right_on,
            left_index=left_index,
            right_index=right_index,
            suffixes=suffixes,
            validate=validate,
        )
        return DataFrame(result)

    def join(
        self,
        other: Union["DataFrame", pd.DataFrame],
        on: Optional[Union[str, List[str]]] = None,
        how: str = "left",
        lsuffix: str = "",
        rsuffix: str = "",
        sort: bool = False,
    ) -> "DataFrame":
        """
        Join columns with other DataFrame.

        Parameters
        ----------
        other : DataFrame
            DataFrame to join with
        on : str or list of str, optional
            Column name(s) to join on
        how : {'left', 'right', 'outer', 'inner'}, default 'left'
            Type of join
        lsuffix : str, default ''
            Suffix for left frame's overlapping columns
        rsuffix : str, default ''
            Suffix for right frame's overlapping columns
        sort : bool, default False
            Sort result by join keys

        Returns
        -------
        DataFrame
            Joined DataFrame
        """
        other_df = other._data if isinstance(other, DataFrame) else other
        result = self._data.join(
            other_df, on=on, how=how, lsuffix=lsuffix, rsuffix=rsuffix, sort=sort
        )
        return DataFrame(result)

    def concat(
        self,
        *others: Union["DataFrame", pd.DataFrame],
        axis: int = 0,
        ignore_index: bool = False,
        verify_integrity: bool = False,
    ) -> "DataFrame":
        """
        Concatenate with other DataFrames.

        Parameters
        ----------
        *others : DataFrame or pd.DataFrame
            DataFrames to concatenate
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Axis to concatenate along
        ignore_index : bool, default False
            Do not use index values
        verify_integrity : bool, default False
            Check whether the new concatenated axis contains duplicates

        Returns
        -------
        DataFrame
            Concatenated DataFrame
        """
        dfs = [self._data] + [df._data if isinstance(df, DataFrame) else df for df in others]
        result = pd.concat(
            dfs, axis=axis, ignore_index=ignore_index, verify_integrity=verify_integrity
        )
        return DataFrame(result)

    # ======================================================================
    # Sorting Methods
    # ======================================================================

    def sort_values(
        self,
        by: Union[str, List[str]],
        axis: int = 0,
        ascending: Union[bool, List[bool]] = True,
        inplace: bool = False,
        na_position: str = "last",
        ignore_index: bool = False,
        key: Optional[Callable] = None,
    ) -> Optional["DataFrame"]:
        """
        Sort by values.

        Parameters
        ----------
        by : str or list of str
            Column name(s) to sort by
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Axis to sort along
        ascending : bool or list of bool, default True
            Sort ascending vs descending
        inplace : bool, default False
            Modify in place
        na_position : {'first', 'last'}, default 'last'
            Position of NAs
        ignore_index : bool, default False
            Do not use index values
        key : callable, optional
            Apply key function before sorting

        Returns
        -------
        DataFrame or None
            Sorted DataFrame or None if inplace=True
        """
        if isinstance(by, list):
            invalid = [col for col in by if col not in self._data.columns]
            if invalid:
                raise PipeFrameColumnError(f"Sort columns {invalid}", list(self._data.columns))
        elif by not in self._data.columns:
            raise PipeFrameColumnError(by, list(self._data.columns))

        if inplace:
            self._data.sort_values(
                by=by,
                axis=axis,
                ascending=ascending,
                inplace=True,
                na_position=na_position,
                ignore_index=ignore_index,
                key=key,
            )
            return None
        result = self._data.sort_values(
            by=by,
            axis=axis,
            ascending=ascending,
            na_position=na_position,
            ignore_index=ignore_index,
            key=key,
        )
        return DataFrame(result)

    def sort_index(
        self,
        axis: int = 0,
        level: Optional[Union[int, str, List]] = None,
        ascending: Union[bool, List[bool]] = True,
        inplace: bool = False,
        na_position: str = "last",
        sort_remaining: bool = True,
        ignore_index: bool = False,
        key: Optional[Callable] = None,
    ) -> Optional["DataFrame"]:
        """Sort by index."""
        if inplace:
            self._data.sort_index(
                axis=axis,
                level=level,
                ascending=ascending,
                inplace=True,
                na_position=na_position,
                sort_remaining=sort_remaining,
                ignore_index=ignore_index,
                key=key,
            )
            return None
        result = self._data.sort_index(
            axis=axis,
            level=level,
            ascending=ascending,
            na_position=na_position,
            sort_remaining=sort_remaining,
            ignore_index=ignore_index,
            key=key,
        )
        return DataFrame(result)

    # ======================================================================
    # Duplicate Handling
    # ======================================================================

    def duplicated(
        self, subset: Optional[List[str]] = None, keep: str = "first"
    ) -> Series:
        """Return boolean Series denoting duplicate rows."""
        if subset:
            invalid = [col for col in subset if col not in self._data.columns]
            if invalid:
                raise PipeFrameColumnError(f"Subset columns {invalid}", list(self._data.columns))
        result = self._data.duplicated(subset=subset, keep=keep)
        return Series(result)

    def drop_duplicates(
        self,
        subset: Optional[List[str]] = None,
        keep: str = "first",
        inplace: bool = False,
        ignore_index: bool = False,
    ) -> Optional["DataFrame"]:
        """Remove duplicate rows."""
        if subset:
            invalid = [col for col in subset if col not in self._data.columns]
            if invalid:
                raise PipeFrameColumnError(f"Subset columns {invalid}", list(self._data.columns))

        if inplace:
            self._data.drop_duplicates(
                subset=subset, keep=keep, inplace=True, ignore_index=ignore_index
            )
            return None
        result = self._data.drop_duplicates(subset=subset, keep=keep, ignore_index=ignore_index)
        return DataFrame(result)

    # ======================================================================
    # Apply Methods
    # ======================================================================

    def apply(
        self,
        func: Callable,
        axis: int = 0,
        raw: bool = False,
        result_type: Optional[str] = None,
        args: tuple = (),
        **kwargs: Any,
    ) -> Union["DataFrame", Series]:
        """
        Apply a function along an axis.

        Parameters
        ----------
        func : callable
            Function to apply to each column or row
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Axis along which to apply
        raw : bool, default False
            Pass ndarray instead of Series
        result_type : {'expand', 'reduce', 'broadcast', None}, optional
            Result type
        args : tuple, default ()
            Positional arguments to pass to func
        **kwargs
            Additional keyword arguments

        Returns
        -------
        DataFrame or Series
            Result of applying func
        """
        result = self._data.apply(
            func, axis=axis, raw=raw, result_type=result_type, args=args, **kwargs
        )
        if isinstance(result, pd.DataFrame):
            return DataFrame(result)
        return Series(result)

    def applymap(self, func: Callable, na_action: Optional[str] = None, **kwargs: Any) -> "DataFrame":
        """
        Apply a function elementwise.

        Parameters
        ----------
        func : callable
            Function to apply
        na_action : {None, 'ignore'}, optional
            How to handle NaN values
        **kwargs
            Additional keyword arguments

        Returns
        -------
        DataFrame
            Transformed DataFrame
        """
        result = self._data.applymap(func, na_action=na_action, **kwargs)
        return DataFrame(result)

    def pipe(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """
        Apply function with pipe syntax (alternative to >>).

        Parameters
        ----------
        func : callable
            Function to apply
        *args
            Positional arguments
        **kwargs
            Keyword arguments

        Returns
        -------
        object
            Result of func(self, *args, **kwargs)
        """
        return func(self, *args, **kwargs)

    # ======================================================================
    # GroupBy
    # ======================================================================

    def groupby(
        self,
        by: Union[str, List[str]],
        level: Optional[Union[int, str, List]] = None,
        as_index: bool = True,
        sort: bool = True,
        group_keys: bool = True,
        observed: bool = False,
        dropna: bool = True,
    ) -> Any:
        """
        Group DataFrame using a mapper or by a Series of columns.

        Parameters
        ----------
        by : str or list of str
            Column name(s) to group by
        level : int, str, or list, optional
            If the axis is a MultiIndex, group by a particular level(s)
        as_index : bool, default True
            Return object with group labels as index
        sort : bool, default True
            Sort group keys
        group_keys : bool, default True
            Add group keys to index
        observed : bool, default False
            For categorical groupby, show only observed values
        dropna : bool, default True
            Do not include NaN in group keys

        Returns
        -------
        GroupBy
            Grouped DataFrame
        """
        from ..verbs.groupby import GroupBy

        # Validate columns
        if isinstance(by, list):
            invalid = [col for col in by if col not in self._data.columns]
            if invalid:
                raise PipeFrameColumnError(f"GroupBy columns {invalid}", list(self._data.columns))
        elif isinstance(by, str) and by not in self._data.columns:
            raise PipeFrameColumnError(by, list(self._data.columns))

        return GroupBy(
            self,
            by=by,
            level=level,
            as_index=as_index,
            sort=sort,
            group_keys=group_keys,
            observed=observed,
            dropna=dropna,
        )

    # ======================================================================
    # I/O Methods
    # ======================================================================

    def to_csv(self, path_or_buf: Optional[str] = None, **kwargs: Any) -> Optional[str]:
        """Write DataFrame to CSV file."""
        return self._data.to_csv(path_or_buf, **kwargs)

    def to_excel(self, excel_writer: Any, sheet_name: str = "Sheet1", **kwargs: Any) -> None:
        """Write DataFrame to Excel file."""
        self._data.to_excel(excel_writer, sheet_name=sheet_name, **kwargs)

    def to_parquet(self, path: str, **kwargs: Any) -> None:
        """Write DataFrame to Parquet file."""
        self._data.to_parquet(path, **kwargs)

    def to_json(self, path_or_buf: Optional[str] = None, **kwargs: Any) -> Optional[str]:
        """Write DataFrame to JSON file."""
        return self._data.to_json(path_or_buf, **kwargs)

    def to_sql(
        self,
        name: str,
        con: Any,
        schema: Optional[str] = None,
        if_exists: str = "fail",
        **kwargs: Any,
    ) -> None:
        """Write DataFrame to SQL database."""
        self._data.to_sql(name, con, schema=schema, if_exists=if_exists, **kwargs)
