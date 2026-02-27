"""
GroupBy implementation for PipeFrame.

Provides group-by-apply-combine functionality with verb interface.
"""

from typing import Any, Callable, Dict, List, Optional, Union

import pandas as pd

from ..core.dataframe import DataFrame
from ..core.series import Series
from ..exceptions import PipeFrameGroupByError, PipeFrameValueError


class GroupBy:
    """
    GroupBy object for aggregation operations.

    Created by DataFrame.groupby() or group_by() verb.

    Examples
    --------
    >>> df >> group_by('category') >> summarize(avg='mean(value)')
    """

    def __init__(
        self,
        df: DataFrame,
        by: Union[str, List[str]],
        level: Optional[Union[int, str, List]] = None,
        as_index: bool = True,
        sort: bool = True,
        group_keys: bool = True,
        observed: bool = False,
        dropna: bool = True,
    ):
        """Initialize GroupBy."""
        self._df = df
        self._by = [by] if isinstance(by, str) else by

        # Get pandas DataFrame
        if isinstance(df, DataFrame):
            pdf = df._data
        else:
            pdf = df

        self._grouped = pdf.groupby(
            by=by,
            level=level,
            as_index=as_index,
            sort=sort,
            group_keys=group_keys,
            observed=observed,
            dropna=dropna,
        )

    def __rshift__(self, other: Callable) -> DataFrame:
        """Enable piping from grouped data."""
        if not callable(other):
            raise PipeFrameGroupByError(f"Cannot pipe to non-callable: {type(other).__name__}")
        return other(self)

    @property
    def groups(self) -> Dict:
        """Return groups dictionary."""
        return self._grouped.groups

    @property
    def ngroups(self) -> int:
        """Return number of groups."""
        return self._grouped.ngroups

    def size(self) -> Series:
        """Return size of each group."""
        return Series(self._grouped.size())

    def count(self) -> DataFrame:
        """Count non-NA values in each group."""
        return DataFrame(self._grouped.count())

    def sum(self, numeric_only: bool = True) -> DataFrame:
        """Sum values in each group."""
        return DataFrame(self._grouped.sum(numeric_only=numeric_only))

    def mean(self, numeric_only: bool = True) -> DataFrame:
        """Mean of each group."""
        return DataFrame(self._grouped.mean(numeric_only=numeric_only))

    def median(self, numeric_only: bool = True) -> DataFrame:
        """Median of each group."""
        return DataFrame(self._grouped.median(numeric_only=numeric_only))

    def min(self, numeric_only: bool = True) -> DataFrame:
        """Minimum of each group."""
        return DataFrame(self._grouped.min(numeric_only=numeric_only))

    def max(self, numeric_only: bool = True) -> DataFrame:
        """Maximum of each group."""
        return DataFrame(self._grouped.max(numeric_only=numeric_only))

    def std(self, ddof: int = 1, numeric_only: bool = True) -> DataFrame:
        """Standard deviation of each group."""
        return DataFrame(self._grouped.std(ddof=ddof, numeric_only=numeric_only))

    def var(self, ddof: int = 1, numeric_only: bool = True) -> DataFrame:
        """Variance of each group."""
        return DataFrame(self._grouped.var(ddof=ddof, numeric_only=numeric_only))

    def first(self) -> DataFrame:
        """First value in each group."""
        return DataFrame(self._grouped.first())

    def last(self) -> DataFrame:
        """Last value in each group."""
        return DataFrame(self._grouped.last())

    def head(self, n: int = 5) -> DataFrame:
        """First n rows of each group."""
        return DataFrame(self._grouped.head(n))

    def tail(self, n: int = 5) -> DataFrame:
        """Last n rows of each group."""
        return DataFrame(self._grouped.tail(n))

    def apply(self, func: Callable, *args: Any, **kwargs: Any) -> DataFrame:
        """Apply function to each group."""
        result = self._grouped.apply(func, *args, **kwargs)
        if isinstance(result, pd.DataFrame):
            return DataFrame(result)
        elif isinstance(result, pd.Series):
            return DataFrame(result.to_frame())
        return result

    def agg(self, func: Union[str, List, Dict], **kwargs: Any) -> DataFrame:
        """Aggregate using one or more operations."""
        result = self._grouped.agg(func, **kwargs)
        return DataFrame(result.reset_index())

    def aggregate(self, func: Union[str, List, Dict], **kwargs: Any) -> DataFrame:
        """Alias for agg."""
        return self.agg(func, **kwargs)

    def transform(self, func: Union[str, Callable], *args: Any, **kwargs: Any) -> DataFrame:
        """Transform values in each group."""
        result = self._grouped.transform(func, *args, **kwargs)
        return DataFrame(result)

    def filter(self, func: Callable, dropna: bool = True) -> DataFrame:
        """Filter groups based on function."""
        result = self._grouped.filter(func, dropna=dropna)
        return DataFrame(result)

    def ungroup(self) -> DataFrame:
        """Return ungrouped DataFrame."""
        return self._df
