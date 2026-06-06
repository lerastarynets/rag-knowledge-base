"""Shared constants used across the API, RAG chain, and ingestors."""

INSUFFICIENT_CONTEXT_MESSAGE = (
    "I could not find a confident answer to your question in the provided documents."
)

FEEDBACK_HEADER_UP = "X-Feedback-Up"
FEEDBACK_HEADER_DOWN = "X-Feedback-Down"

SOURCE_TYPE_PDF = "pdf"
SOURCE_TYPE_DOCX = "docx"
SOURCE_TYPE_URL = "url"
SOURCE_TYPE_YOUTUBE = "youtube"
