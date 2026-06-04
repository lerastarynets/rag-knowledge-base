"""Chain package for composing RAG (Retrieval-Augmented Generation) pipelines."""

from .rag import rag_chain

RAG_CHAIN = rag_chain()

__all__ = ["RAG_CHAIN", "rag_chain"]
