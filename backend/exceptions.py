"""Exceptions module: defines custom exceptions for the application."""


class InsufficientContextError(Exception):
    """Raised when the context is insufficient to answer the question."""

    pass


class IngestionError(Exception):
    """Raised when a document source is invalid or yields unusable content."""

    pass
