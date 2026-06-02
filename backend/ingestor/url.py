"""URL ingestor: fetches and parses web pages into text chunks for indexing."""

from __future__ import annotations

import httpx
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from pydantic import HttpUrl

from exceptions import IngestionError
from ingestor.pipeline import ingest_documents
from ingestor.validation import assert_content_quality, reject_login_or_error_title

HTTP_TIMEOUT_SECONDS = 30.0

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
}

ALLOWED_CONTENT_TYPES = frozenset(
    {
        "text/html",
        "application/xhtml+xml",
    }
)


def _html_to_documents(html: str, *, source: str) -> list[Document]:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.title
    title = title_tag.get_text(strip=True) if title_tag else ""
    reject_login_or_error_title(title)

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    if not text:
        return []

    return [
        Document(
            page_content=text,
            metadata={"source": source, "title": title},
        )
    ]


async def ingest_url(url: HttpUrl) -> None:
    url_str = str(url)

    try:
        async with httpx.AsyncClient(
            timeout=HTTP_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers=BROWSER_HEADERS
        ) as client:
            response = await client.get(url_str)
            response.raise_for_status()
            final_url = str(response.url)
            content_type = response.headers.get("content-type", "").split(";")[0].strip().lower()
            html = response.text
    except httpx.HTTPStatusError as exc:
        raise IngestionError(f"URL returned HTTP {exc.response.status_code}: {url_str}") from exc
    except httpx.HTTPError as exc:
        raise IngestionError(f"Failed to fetch URL: {url_str}") from exc

    if content_type not in ALLOWED_CONTENT_TYPES:
        raise IngestionError(
            f"Unsupported content type {content_type!r} for URL: {final_url}"
        )

    documents = _html_to_documents(html, source=final_url)
    if not documents:
        raise IngestionError(f"No readable content at URL: {final_url}")

    assert_content_quality(documents)

    print("ingesting url", final_url)
    await ingest_documents(documents, file_name=documents[0].metadata.get("title") or final_url)
    print("url ingested")
