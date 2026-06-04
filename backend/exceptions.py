"""Exceptions module: defines custom exceptions for the application."""


class InsufficientContextError(Exception):
    """Raised when the context is insufficient to answer the question."""

    pass


class IngestionError(Exception):
    """Raised when a document source is invalid or yields unusable content."""

    pass


class UnsupportedFileTypeError(IngestionError):
    """Raised when an uploaded file has an unsupported MIME type."""

    pass
