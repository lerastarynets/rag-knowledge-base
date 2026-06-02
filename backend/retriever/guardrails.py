"""Validate retrieval results for safety and relevance."""

from langchain_core.documents import Document

from exceptions import InsufficientContextError

RELEVANCE_SCORE_THRESHOLD = 0.3


def assert_relevance(results: list[Document]) -> list[Document]:
    relevance_score = results[0].metadata.get("relevance_score")
    if not relevance_score or float(relevance_score or 0) < RELEVANCE_SCORE_THRESHOLD:
        raise InsufficientContextError(
            f"Top relevance score {relevance_score} is below "
            f"threshold {RELEVANCE_SCORE_THRESHOLD}"
        )
    return results
