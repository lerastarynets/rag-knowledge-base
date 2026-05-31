"""Validation helpers for ingestors."""

from __future__ import annotations

import re
from typing import Literal

from langchain_core.documents import Document

from exceptions import IngestionError
MIN_CONTENT_LENGTH = 200

VIDEO_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{11}$")

YOUTUBE_WATCH_PATTERN = re.compile(
    r"youtube\.com/watch\?(?:[^&]*&)*v=([a-zA-Z0-9_-]{11})"
)
YOUTUBE_SHORT_PATTERN = re.compile(r"youtu\.be/([a-zA-Z0-9_-]{11})")
YOUTUBE_EMBED_PATTERN = re.compile(r"youtube\.com/embed/([a-zA-Z0-9_-]{11})")
YOUTUBE_V_PATH_PATTERN = re.compile(r"youtube\.com/v/([a-zA-Z0-9_-]{11})")
YOUTUBE_SHORTS_PATTERN = re.compile(r"youtube\.com/shorts/([a-zA-Z0-9_-]{11})")

YOUTUBE_URL_PATTERNS = (
    YOUTUBE_WATCH_PATTERN,
    YOUTUBE_SHORT_PATTERN,
    YOUTUBE_EMBED_PATTERN,
    YOUTUBE_V_PATH_PATTERN,
    YOUTUBE_SHORTS_PATTERN,
)

ERROR_PAGE_MARKERS = (
    "404 not found",
    "403 forbidden",
    "access denied",
    "page not found",
)

CONTENT_DENYLIST = ERROR_PAGE_MARKERS + (
    "sign in to continue",
    "log in to continue",
)

YOUTUBE_BOILERPLATE_MARKERS = (
    "presscopyright",
    "how youtube works",
    "test new features",
    "creatorsadvertise",
)

LOGIN_TITLE_MARKERS = ERROR_PAGE_MARKERS + (
    "sign in",
    "log in",
    "login",
)


def is_youtube_domain(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url


def extract_youtube_video_id(url: str) -> str | None:
    """Return an 11-character YouTube video id from a URL, or None."""
    for pattern in YOUTUBE_URL_PATTERNS:
        match = pattern.search(url)
        if match:
            return match.group(1)
    return None


def assert_content_quality(
    documents: list[Document],
    *,
    source: Literal["url", "youtube"] = "url",
) -> None:
    """Reject documents that look like error pages or boilerplate."""
    if not documents:
        raise IngestionError("No content to index")

    combined = "\n".join(doc.page_content for doc in documents).strip()
    if len(combined) < MIN_CONTENT_LENGTH:
        raise IngestionError(
            f"Content too short to index (minimum {MIN_CONTENT_LENGTH} characters)"
        )

    denylist = CONTENT_DENYLIST
    if source == "youtube":
        denylist = CONTENT_DENYLIST + YOUTUBE_BOILERPLATE_MARKERS

    lowered = combined.lower()
    for marker in denylist:
        if marker in lowered:
            raise IngestionError("Content looks like an error or boilerplate page")


def reject_login_or_error_title(title: str) -> None:
    """Reject pages whose HTML title looks like login or error screens."""
    normalized = title.strip().lower()
    if not normalized:
        return
    for marker in LOGIN_TITLE_MARKERS:
        if marker in normalized:
            raise IngestionError(f"Page title indicates blocked or error content: {title!r}")
