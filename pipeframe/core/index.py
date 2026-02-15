"""
PipeFrame Index implementation - enhanced pandas Index wrapper.

This module provides an Index class that wraps pandas Index objects.
"""

from typing import Any, List, Optional, Union

import numpy as np
import pandas as pd


class Index:
    """
    PipeFrame Index - Immutable sequence used for indexing and alignment.

    Parameters
    ----------
    data : array-like (1-dimensional)
    dtype : dtype, default None
    copy : bool, default False
    name : object, default None
    """

    def __init__(
        self,
        data: Any = None,
        dtype: Optional[Any] = None,
        copy: bool = False,
        name: Optional[str] = None,
    ):
        """Initialize a PipeFrame Index."""
        if isinstance(data, pd.Index):
            self._data = data.copy() if copy else data
        else:
            self._data = pd.Index(data, dtype=dtype, copy=copy, name=name)

    def __getitem__(self, key: Any) -> Union["Index", Any]:
        """Get item from Index."""
        result = self._data[key]
        if isinstance(result, pd.Index):
            return Index(result)
        return result

    def __len__(self) -> int:
        """Return length of Index."""
        return len(self._data)

    def __repr__(self) -> str:
        """String representation."""
        return f"<pipeframe.Index>\n{self._data.__repr__()}"

    def __str__(self) -> str:
        """String representation for printing."""
        return self._data.__str__()

    @property
    def values(self) -> np.ndarray:
        """Return numpy array representation."""
        return self._data.values

    @property
    def name(self) -> Optional[str]:
        """Return the name of the Index."""
        return self._data.name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name of the Index."""
        self._data.name = value

    @property
    def dtype(self) -> Any:
        """Return the data type."""
        return self._data.dtype

    @property
    def shape(self) -> tuple:
        """Return shape of Index."""
        return self._data.shape

    @property
    def size(self) -> int:
        """Return the number of elements."""
        return self._data.size

    def to_pandas(self) -> pd.Index:
        """Convert to pandas Index."""
        return self._data.copy()

    @classmethod
    def from_pandas(cls, index: pd.Index) -> "Index":
        """Create from pandas Index."""
        return cls(index)

    def to_numpy(self) -> np.ndarray:
        """Convert to numpy array."""
        return self._data.to_numpy()

    def to_list(self) -> List[Any]:
        """Convert to Python list."""
        return self._data.tolist()

    def copy(self, deep: bool = True) -> "Index":
        """Copy Index."""
        return Index(self._data.copy(deep=deep))

    def unique(self) -> "Index":
        """Return unique values."""
        return Index(self._data.unique())

    def nunique(self, dropna: bool = True) -> int:
        """Return number of unique elements."""
        return self._data.nunique(dropna=dropna)

    def is_unique(self) -> bool:
        """Return whether Index has unique values."""
        return self._data.is_unique

    def duplicated(self, keep: str = "first") -> np.ndarray:
        """Return boolean array denoting duplicate values."""
        return self._data.duplicated(keep=keep)
