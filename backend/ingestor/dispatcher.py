"""File dispatcher: dispatches files to the appropriate ingestor."""

from pydantic import HttpUrl

from exceptions import IngestionError
from ingestor.docx import ingest_docx
from ingestor.pdf import ingest_pdf
from ingestor.url import ingest_url
from ingestor.validation import extract_youtube_video_id, is_youtube_domain
from ingestor.youtube import ingest_youtube


async def file_dispatcher(
    file_path: str,
    file_content_type: str,
    file_name: str,
) -> None:
    if (
        file_content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        await ingest_docx(file_path, file_name)
    elif file_content_type == "application/pdf":
        await ingest_pdf(file_path, file_name)
    else:
        raise ValueError(f"Unsupported file type: {file_content_type}")


async def url_dispatcher(url: HttpUrl) -> None:
    url_str = str(url)
    if is_youtube_domain(url_str):
        if extract_youtube_video_id(url_str) is None:
            raise IngestionError(
                "Invalid YouTube URL: could not extract a valid 11-character video ID"
            )
        await ingest_youtube(url)
    else:
        await ingest_url(url)
