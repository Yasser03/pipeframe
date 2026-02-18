"""
PipeFrame: Pipe Your Data Naturally
====================================

A comprehensive data manipulation library with grammar-based syntax.
Transform your data workflows into readable, maintainable code using
the power of the pipe operator.

Basic usage:
    >>> from pipeframe import *
    >>> result = (df
    ...     >> filter('age > 21')
    ...     >> group_by('city')
    ...     >> summarize(avg_income='mean(income)')
    ...     >> arrange('-avg_income')
    ... )

Core verbs:
    define()    : Create or modify columns
    filter()    : Filter rows based on conditions
    select()    : Choose specific columns
    arrange()   : Sort data
    group_by()  : Group data for aggregation
    summarize() : Reduce groups to summaries
    rename()    : Rename columns
    distinct()  : Get unique rows
"""

__version__ = "0.2.0"
__author__ = "PipeFrame Team"
__email__ = "team@pipeframe.dev"
__license__ = "MIT"

# Core data structures
from .core.dataframe import DataFrame
from .core.series import Series
from .core.index import Index

# Core verbs
from .verbs.manipulate import (
    arrange,
    case_when,
    contains,
    define,
    desc,
    distinct,
    ends_with,
    filter,
    filter_rows,
    group_by,
    if_else,
    matches,
    mutate,
    one_of,
    rename,
    select,
    slice_rows,
    starts_with,
    summarize,
    tail,
    ungroup,
)

# Utility operations
from .utils.helpers import (
    Snapshot,
    peek,
    profile_pipeline,
)

# GroupBy
from .verbs.groupby import GroupBy

# Reshape operations
from .verbs.reshape import (
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

# I/O operations
from .io.readers import (
    read_clipboard,
    read_csv,
    read_excel,
    read_feather,
    read_html,
    read_json,
    read_parquet,
    read_sql,
    read_sql_query,
    read_sql_table,
    read_tsv,
    to_csv,
    to_excel,
    to_json,
    to_parquet,
)

# Export public interface
__all__ = [
    # Core classes
    "DataFrame",
    "Series",
    "Index",
    # Version info
    "__version__",
    # Manipulation verbs
    "define",
    "mutate",
    "select",
    "filter",
    "filter_rows",
    "arrange",
    "group_by",
    "summarize",
    "ungroup",
    "rename",
    "distinct",
    "slice_rows",
    # Conditional functions
    "if_else",
    "case_when",
    # Selection helpers
    "starts_with",
    "ends_with",
    "contains",
    "matches",
    "one_of",
    "desc",
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
    # I/O operations
    "read_csv",
    "read_tsv",
    "read_excel",
    "read_json",
    "read_parquet",
    "read_feather",
    "read_sql",
    "read_sql_table",
    "read_sql_query",
    "read_clipboard",
    "read_html",
    "to_csv",
    "to_excel",
    "to_json",
    "to_parquet",
    # Utilities
    "peek",
    "Snapshot",
    "profile_pipeline",
]
