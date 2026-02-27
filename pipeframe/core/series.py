"""
PipeFrame Series implementation - enhanced pandas Series wrapper.

This module provides a Series class that wraps pandas Series and integrates
with the PipeFrame ecosystem.
"""

from typing import Any, Callable, List, Optional, Union

import numpy as np
import pandas as pd

from ..exceptions import PipeFrameTypeError


class Series:
    """
    PipeFrame Series - A grammar-compatible one-dimensional labeled array.

    Wraps pandas Series to provide consistent interface with DataFrame.

    Parameters
    ----------
    data : array-like, Iterable, dict, or scalar value
        Contains data stored in Series
    index : array-like or Index
        Index to use for resulting Series
    dtype : str, numpy.dtype, or ExtensionDtype, optional
        Data type for the output Series
    name : str, optional
        Name to give to the Series
    copy : bool, default False
        Copy input data

    Examples
    --------
    >>> s = Series([1, 2, 3, 4])
    >>> s = Series({'a': 1, 'b': 2, 'c': 3})
    >>> s = Series(5, index=['a', 'b', 'c'])
    """

    def __init__(
        self,
        data: Any = None,
        index: Optional[Any] = None,
        dtype: Optional[Any] = None,
        name: Optional[str] = None,
        copy: bool = False,
    ):
        """Initialize a PipeFrame Series."""
        if isinstance(data, pd.Series):
            self._data = data.copy() if copy else data
        else:
            self._data = pd.Series(data, index=index, dtype=dtype, name=name, copy=copy)

    # ======================================================================
    # Magic Methods
    # ======================================================================

    def __getitem__(self, key: Any) -> Union["Series", Any]:
        """Get item from Series."""
        result = self._data[key]
        if isinstance(result, pd.Series):
            return Series(result)
        return result

    def __setitem__(self, key: Any, value: Any) -> None:
        """Set item in Series."""
        self._data[key] = value

    def __len__(self) -> int:
        """Return length of Series."""
        return len(self._data)

    def __repr__(self) -> str:
        """String representation."""
        return f"<pipeframe.Series>\n{self._data.__repr__()}"

    def __str__(self) -> str:
        """String representation for printing."""
        return self._data.__str__()

    def __iter__(self):
        """Iterate over values in the Series."""
        return iter(self._data)

    # Arithmetic operations
    def __add__(self, other: Any) -> "Series":
        """Addition."""
        return Series(self._data + other)

    def __sub__(self, other: Any) -> "Series":
        """Subtraction."""
        return Series(self._data - other)

    def __mul__(self, other: Any) -> "Series":
        """Multiplication."""
        return Series(self._data * other)

    def __truediv__(self, other: Any) -> "Series":
        """Division."""
        return Series(self._data / other)

    def __floordiv__(self, other: Any) -> "Series":
        """Floor division."""
        return Series(self._data // other)

    def __mod__(self, other: Any) -> "Series":
        """Modulo."""
        return Series(self._data % other)

    def __pow__(self, other: Any) -> "Series":
        """Power."""
        return Series(self._data**other)

    # Comparison operations
    def __eq__(self, other: Any) -> "Series":  # type: ignore
        """Equality."""
        return Series(self._data == other)

    def __ne__(self, other: Any) -> "Series":  # type: ignore
        """Inequality."""
        return Series(self._data != other)

    def __lt__(self, other: Any) -> "Series":
        """Less than."""
        return Series(self._data < other)

    def __le__(self, other: Any) -> "Series":
        """Less than or equal."""
        return Series(self._data <= other)

    def __gt__(self, other: Any) -> "Series":
        """Greater than."""
        return Series(self._data > other)

    def __ge__(self, other: Any) -> "Series":
        """Greater than or equal."""
        return Series(self._data >= other)

    # ======================================================================
    # Properties
    # ======================================================================

    @property
    def values(self) -> np.ndarray:
        """Return numpy array representation."""
        return self._data.values

    @property
    def index(self) -> pd.Index:
        """Return the index."""
        return self._data.index

    @property
    def dtype(self) -> Any:
        """Return the data type."""
        return self._data.dtype

    @property
    def shape(self) -> tuple:
        """Return shape of Series."""
        return self._data.shape

    @property
    def name(self) -> Optional[str]:
        """Return the name of the Series."""
        return self._data.name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name of the Series."""
        self._data.name = value

    @property
    def size(self) -> int:
        """Return the number of elements."""
        return self._data.size

    # ======================================================================
    # Conversion Methods
    # ======================================================================

    def to_pandas(self) -> pd.Series:
        """Convert to pandas Series."""
        return self._data.copy()

    @classmethod
    def from_pandas(cls, series: pd.Series) -> "Series":
        """Create from pandas Series."""
        return cls(series)

    def to_numpy(self) -> np.ndarray:
        """Convert to numpy array."""
        return self._data.to_numpy()

    def to_list(self) -> List[Any]:
        """Convert to Python list."""
        return self._data.tolist()

    def to_frame(self, name: Optional[str] = None) -> "DataFrame":
        """
        Convert Series to DataFrame.

        Parameters
        ----------
        name : str, optional
            Name to use for the column. If None, uses the current series name.

        Returns
        -------
        DataFrame
            DataFrame representation of the Series
        """
        from .dataframe import DataFrame

        return DataFrame(self._data.to_frame(name))

    def copy(self, deep: bool = True) -> "Series":
        """Copy Series."""
        return Series(self._data.copy(deep=deep))

    # ======================================================================
    # Aggregation Methods
    # ======================================================================

    def sum(self, skipna: bool = True) -> Any:
        """Return sum of values."""
        return self._data.sum(skipna=skipna)

    def mean(self, skipna: bool = True) -> float:
        """Return mean of values."""
        return self._data.mean(skipna=skipna)

    def median(self, skipna: bool = True) -> float:
        """Return median of values."""
        return self._data.median(skipna=skipna)

    def std(self, skipna: bool = True, ddof: int = 1) -> float:
        """Return standard deviation."""
        return self._data.std(skipna=skipna, ddof=ddof)

    def var(self, skipna: bool = True, ddof: int = 1) -> float:
        """Return variance."""
        return self._data.var(skipna=skipna, ddof=ddof)

    def min(self, skipna: bool = True) -> Any:
        """Return minimum value."""
        return self._data.min(skipna=skipna)

    def max(self, skipna: bool = True) -> Any:
        """Return maximum value."""
        return self._data.max(skipna=skipna)

    def count(self) -> int:
        """Count non-NA values."""
        return self._data.count()

    def nunique(self, dropna: bool = True) -> int:
        """Count unique values."""
        return self._data.nunique(dropna=dropna)

    # ======================================================================
    # Information Methods
    # ======================================================================

    def head(self, n: int = 5) -> "Series":
        """Return first n values."""
        return Series(self._data.head(n))

    def tail(self, n: int = 5) -> "Series":
        """Return last n values."""
        return Series(self._data.tail(n))

    def describe(self, percentiles: Optional[List[float]] = None) -> "Series":
        """Generate descriptive statistics."""
        return Series(self._data.describe(percentiles=percentiles))

    def unique(self) -> np.ndarray:
        """Return unique values."""
        return self._data.unique()

    def value_counts(
        self,
        normalize: bool = False,
        sort: bool = True,
        ascending: bool = False,
        dropna: bool = True,
    ) -> "Series":
        """Return value counts."""
        return Series(
            self._data.value_counts(
                normalize=normalize, sort=sort, ascending=ascending, dropna=dropna
            )
        )

    # ======================================================================
    # Missing Data
    # ======================================================================

    def isna(self) -> "Series":
        """Detect missing values."""
        return Series(self._data.isna())

    def isnull(self) -> "Series":
        """Detect missing values (alias for isna)."""
        return self.isna()

    def notna(self) -> "Series":
        """Detect non-missing values."""
        return Series(self._data.notna())

    def fillna(
        self, value: Any = None, method: Optional[str] = None, inplace: bool = False
    ) -> Optional["Series"]:
        """Fill missing values."""
        if inplace:
            self._data.fillna(value=value, method=method, inplace=True)
            return None
        return Series(self._data.fillna(value=value, method=method))

    def dropna(self, inplace: bool = False) -> Optional["Series"]:
        """Remove missing values."""
        if inplace:
            self._data.dropna(inplace=True)
            return None
        return Series(self._data.dropna())

    # ======================================================================
    # Apply & Transform
    # ======================================================================

    def apply(self, func: Callable, convert_dtype: bool = True, args: tuple = ()) -> "Series":
        """Apply a function along the Series."""
        return Series(self._data.apply(func, convert_dtype=convert_dtype, args=args))

    def map(self, arg: Union[dict, Callable], na_action: Optional[str] = None) -> "Series":
        """Map values using a mapping correspondence."""
        return Series(self._data.map(arg, na_action=na_action))

    # ======================================================================
    # Sorting
    # ======================================================================

    def sort_values(
        self, ascending: bool = True, inplace: bool = False, na_position: str = "last"
    ) -> Optional["Series"]:
        """Sort by values."""
        if inplace:
            self._data.sort_values(ascending=ascending, inplace=True, na_position=na_position)
            return None
        return Series(self._data.sort_values(ascending=ascending, na_position=na_position))

    def sort_index(
        self, ascending: bool = True, inplace: bool = False, na_position: str = "last"
    ) -> Optional["Series"]:
        """Sort by index."""
        if inplace:
            self._data.sort_index(ascending=ascending, inplace=True, na_position=na_position)
            return None
        return Series(self._data.sort_index(ascending=ascending, na_position=na_position))

    # ======================================================================
    # String Methods (for object dtype)
    # ======================================================================

    @property
    def str(self) -> Any:
        """Accessor for string methods."""
        return self._data.str
