"""
Basic tests for PipeFrame core functionality.

Author: Dr. Yasser Mustafa
"""

import pytest
import pandas as pd
from pipeframe import (
    DataFrame,
    filter,
    define,
    select,
    arrange,
    group_by,
    summarize,
    head,
    tail,
    shape,
)
from pipeframe.exceptions import PipeFrameColumnError, PipeFrameExpressionError


class TestDataFrame:
    """Test DataFrame creation and basic operations."""

    def test_create_dataframe(self):
        """Test DataFrame creation from dict."""
        df = DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        assert len(df) == 3
        assert len(df.columns) == 2

    def test_from_pandas(self):
        """Test creating DataFrame from pandas."""
        pdf = pd.DataFrame({"a": [1, 2, 3]})
        df = DataFrame(pdf)
        assert len(df) == 3

    def test_pipe_operator(self):
        """Test pipe operator works."""
        df = DataFrame({"x": [1, 2, 3]})
        result = df >> filter("x > 1")
        assert len(result) == 2


class TestFilter:
    """Test filter operations."""

    def test_filter_basic(self):
        """Test basic filtering."""
        df = DataFrame({"x": [1, 2, 3, 4, 5]})
        result = df >> filter("x > 2")
        assert len(result) == 3
        assert result["x"].min() > 2

    def test_filter_complex(self):
        """Test complex filter conditions."""
        df = DataFrame({"x": [1, 2, 3, 4], "y": [10, 20, 30, 40]})
        result = df >> filter("(x > 1) & (y < 35)")
        assert len(result) == 2

    def test_filter_empty_result(self):
        """Test filter returning empty DataFrame."""
        df = DataFrame({"x": [1, 2, 3]})
        result = df >> filter("x > 100")
        assert len(result) == 0

    def test_filter_invalid_column(self):
        """Test error on invalid column."""
        df = DataFrame({"x": [1, 2, 3]})
        with pytest.raises(Exception):  # Will raise query error
            df >> filter("nonexistent > 2")


class TestDefine:
    """Test column definition."""

    def test_define_single_column(self):
        """Test creating single column."""
        df = DataFrame({"x": [1, 2, 3]})
        result = df >> define(y="x * 2")
        assert "y" in result.columns
        assert list(result["y"]) == [2, 4, 6]

    def test_define_multiple_columns(self):
        """Test creating multiple columns."""
        df = DataFrame({"x": [1, 2, 3]})
        result = df >> define(y="x * 2", z="x + 10")
        assert "y" in result.columns
        assert "z" in result.columns

    def test_define_overwrite(self):
        """Test overwriting existing column."""
        df = DataFrame({"x": [1, 2, 3]})
        result = df >> define(x="x * 10")
        assert list(result["x"]) == [10, 20, 30]


class TestSelect:
    """Test column selection."""

    def test_select_single(self):
        """Test selecting single column."""
        df = DataFrame({"x": [1, 2], "y": [3, 4], "z": [5, 6]})
        result = df >> select("x")
        assert len(result.columns) == 1
        assert "x" in result.columns

    def test_select_multiple(self):
        """Test selecting multiple columns."""
        df = DataFrame({"x": [1, 2], "y": [3, 4], "z": [5, 6]})
        result = df >> select("x", "z")
        assert len(result.columns) == 2
        assert "x" in result.columns
        assert "z" in result.columns

    def test_select_invalid(self):
        """Test error on invalid column."""
        df = DataFrame({"x": [1, 2], "y": [3, 4]})
        with pytest.raises(PipeFrameColumnError):
            df >> select("nonexistent")


class TestArrange:
    """Test sorting."""

    def test_arrange_ascending(self):
        """Test ascending sort."""
        df = DataFrame({"x": [3, 1, 2]})
        result = df >> arrange("x")
        assert list(result["x"]) == [1, 2, 3]

    def test_arrange_descending(self):
        """Test descending sort."""
        df = DataFrame({"x": [1, 3, 2]})
        result = df >> arrange("-x")
        assert list(result["x"]) == [3, 2, 1]


class TestGroupBy:
    """Test grouping and summarization."""

    def test_groupby_summarize(self):
        """Test basic group and summarize."""
        df = DataFrame({"category": ["A", "B", "A", "B"], "value": [10, 20, 30, 40]})
        result = df >> group_by("category") >> summarize(total="sum(value)")
        assert len(result) == 2
        assert "total" in result.columns


class TestNewVerbs:
    """Test newly added head, tail, and shape verbs."""

    def test_head_basic(self):
        """Test head() verb."""
        df = DataFrame({"x": range(10)})
        result = df >> head(3)
        assert len(result) == 3
        assert list(result["x"]) == [0, 1, 2]

    def test_tail_basic(self):
        """Test tail() verb."""
        df = DataFrame({"x": range(10)})
        result = df >> tail(3)
        assert len(result) == 3
        assert list(result["x"]) == [7, 8, 9]

    def test_shape_basic(self):
        """Test shape() verb."""
        df = DataFrame({"x": [1, 2], "y": [3, 4]})
        result = df >> shape()
        assert result == (2, 2)


class TestSecurity:
    """Test security features."""

    def test_blocks_dangerous_import(self):
        """Test that __import__ is blocked."""
        df = DataFrame({"x": [1, 2, 3]})
        with pytest.raises(PipeFrameExpressionError):
            df >> define(bad="__import__('os').system('ls')")

    def test_blocks_exec(self):
        """Test that exec is blocked."""
        df = DataFrame({"x": [1, 2, 3]})
        with pytest.raises(PipeFrameExpressionError):
            df >> define(bad="exec('print(1)')")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
