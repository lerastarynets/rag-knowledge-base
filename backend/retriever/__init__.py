"""Retriever package for searching and retrieving relevant document chunks."""

from .guardrails import assert_relevance
from .search import search

__all__ = ["search", "assert_relevance"]
