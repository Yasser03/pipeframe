"""
I/O operations for PipeFrame.

This module provides functions for reading and writing data in various formats.
"""

from .readers import (
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

__all__ = [
    # Readers
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
    # Writers
    "to_csv",
    "to_excel",
    "to_json",
    "to_parquet",
]
