"""
Core manipulation verbs for PipeFrame.

This module provides all the data manipulation verbs including:
- Column operations (define, select, rename)
- Row operations (filter, arrange, slice, distinct)
- GroupBy operations
- Reshape operations
"""

from .groupby import GroupBy
from .reshape import (
    gather,
    melt,
    pivot,
    pivot_longer,
    pivot_table,
    pivot_wider,
    separate,
    spread,
    stack,
    transpose,
    unite,
    unstack,
)

# Note: manipulate verbs will be imported when that module is created
# from .manipulate import (
#     arrange, case_when, contains, define, desc, distinct,
#     ends_with, filter, filter_rows, group_by, if_else,
#     matches, mutate, one_of, rename, select, slice_rows,
#     starts_with, summarize, ungroup
# )

__all__ = [
    # GroupBy
    "GroupBy",
    # Reshape operations
    "pivot_wider",
    "pivot_longer",
    "pivot",
    "pivot_table",
    "melt",
    "gather",
    "stack",
    "unstack",
    "spread",
    "separate",
    "unite",
    "transpose",
]
