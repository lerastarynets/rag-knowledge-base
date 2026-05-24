"""Ingestor package for loading and parsing documents from various sources."""
from ingestor.dispatcher import file_dispatcher, url_dispatcher

__all__ = ["file_dispatcher", "url_dispatcher"]