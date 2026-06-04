"""Validate retrieval results for safety and relevance."""

from langchain_core.documents import Document

from exceptions import InsufficientContextError

RELEVANCE_SCORE_THRESHOLD = 0.3


def assert_relevance(results: list[Document]) -> list[Document]:
    if not results:
        raise InsufficientContextError("No documents retrieved")

    relevance_score = results[0].metadata.get("relevance_score")
    if relevance_score is None:
        raise InsufficientContextError(
            f"Top relevance score is missing (threshold {RELEVANCE_SCORE_THRESHOLD})"
        )

    score = float(relevance_score)
    if score < RELEVANCE_SCORE_THRESHOLD:
        raise InsufficientContextError(
            f"Top relevance score {score} is below "
            f"threshold {RELEVANCE_SCORE_THRESHOLD}"
        )
    return results
