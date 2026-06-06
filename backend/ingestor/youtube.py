"""YouTube ingestor: fetches transcripts from YouTube videos for indexing."""

from __future__ import annotations

import asyncio
import logging

import httpx
from langchain_community.document_loaders import YoutubeLoader
from pydantic import HttpUrl

from constants import SOURCE_TYPE_YOUTUBE
from exceptions import IngestionError
from ingestor.pipeline import ingest_documents
from ingestor.validation import assert_content_quality, extract_youtube_video_id

logger = logging.getLogger(__name__)

HTTP_TIMEOUT_SECONDS = 15.0


async def _fetch_video_info(url: str) -> dict[str, str]:
    """Fetch title and author via YouTube oEmbed."""
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS) as client:
            response = await client.get(
                "https://www.youtube.com/oembed",
                params={"url": url, "format": "json"},
            )
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as exc:
        raise IngestionError(f"YouTube video not found or unavailable: {url}") from exc
    except httpx.HTTPError as exc:
        raise IngestionError(f"Failed to fetch YouTube metadata: {url}") from exc

    return {
        "title": data.get("title") or "Unknown",
        "author": data.get("author_name") or "Unknown",
    }


async def ingest_youtube(url: HttpUrl) -> None:
    url_str = str(url)

    video_id = extract_youtube_video_id(url_str)
    if video_id is None:
        raise IngestionError("Invalid YouTube URL: video id must be 11 characters")

    canonical_url = f"https://www.youtube.com/watch?v={video_id}"
    video_info = await _fetch_video_info(canonical_url)

    loader = YoutubeLoader.from_youtube_url(canonical_url, add_video_info=False)
    documents = await asyncio.to_thread(loader.load)
    if not documents:
        raise IngestionError("No transcript available for this video")

    assert_content_quality(documents, source="youtube")

    for document in documents:
        document.metadata.update(video_info)
        document.metadata["video_id"] = video_id
        document.metadata["source_type"] = SOURCE_TYPE_YOUTUBE

    logger.info("ingesting youtube: %s", video_info.get("title"))
    await ingest_documents(documents, file_name=video_info["title"])
    logger.info("youtube ingested")
