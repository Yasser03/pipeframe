"""
Custom exception hierarchy for the PipeFrame package.

This module defines all custom exceptions used throughout PipeFrame,
providing better error messages and exception handling.
"""

from typing import List, Optional


class PipeFrameError(Exception):
    """Base exception for all PipeFrame-related errors."""

    pass


class PipeFrameTypeError(PipeFrameError, TypeError):
    """Raised when an operation receives an argument of inappropriate type."""

    def __init__(
        self, message: str, expected_type: Optional[type] = None, got_type: Optional[type] = None
    ):
        if expected_type and got_type:
            message = f"{message} Expected {expected_type.__name__}, got {got_type.__name__}"
        super().__init__(message)


class PipeFrameValueError(PipeFrameError, ValueError):
    """Raised when an operation receives an argument with inappropriate value."""

    pass


class PipeFrameColumnError(PipeFrameError, KeyError):
    """Raised when a referenced column doesn't exist in the DataFrame."""

    def __init__(self, column: str, available: Optional[List[str]] = None):
        message = f"Column '{column}' not found"
        if available:
            message += f". Available columns: {available}"
        super().__init__(message)


class PipeFrameExpressionError(PipeFrameError):
    """Raised when an expression cannot be evaluated."""

    def __init__(self, expression: str, reason: Optional[str] = None):
        message = f"Invalid expression: '{expression}'"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


class PipeFrameGroupByError(PipeFrameError):
    """Raised when a group-by operation fails."""

    pass


class PipeFrameIOError(PipeFrameError, IOError):
    """Raised when an I/O operation fails."""

    pass


class PipeFrameEmptyDataError(PipeFrameError):
    """Raised when an operation requires non-empty data but receives empty DataFrame."""

    def __init__(self, operation: str):
        super().__init__(f"Cannot perform '{operation}' on empty DataFrame")
