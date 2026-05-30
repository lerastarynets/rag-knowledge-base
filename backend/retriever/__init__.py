"""Retriever package for searching and retrieving relevant document chunks."""

from .search import search
from .guardrails import assert_relevance

__all__ = ["search", "assert_relevance"]