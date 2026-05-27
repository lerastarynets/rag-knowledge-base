"""Guardrails module: validates and filters retrieval results for safety and relevance."""
from langchain_core.documents import Document

class InsufficientContextError(Exception):
    pass

RELEVANCE_SCORE_THRESHOLD = 0.3

def assert_relevance(results: list[Document]) -> None:
    relevance_score = results[0].metadata.get("relevance_score")
    if not relevance_score or float(relevance_score or 0) < RELEVANCE_SCORE_THRESHOLD:
        raise InsufficientContextError(f"Top relevance score {relevance_score} is below threshold {RELEVANCE_SCORE_THRESHOLD}")