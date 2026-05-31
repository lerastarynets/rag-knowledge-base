"""File dispatcher: dispatches files to the appropriate ingestor."""
from pydantic import HttpUrl
import re
from ingestor.youtube import ingest_youtube
from ingestor.url import ingest_url
from ingestor.docx import ingest_docx
from ingestor.pdf import ingest_pdf

def is_youtube_url(url: HttpUrl) -> bool:
    # Regex to match common YouTube URL patterns
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )

    match = re.match(youtube_regex, str(url))
    return match is not None

async def file_dispatcher(file_path: str, file_content_type: str, file_name: str,) -> None:
    if file_content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        await ingest_docx(file_path, file_name)
    elif file_content_type == "application/pdf":
        await ingest_pdf(file_path, file_name)
    else:
        raise ValueError(f"Unsupported file type: {file_content_type}")
    
async def url_dispatcher(url: HttpUrl) -> None:
    if is_youtube_url(url):
        await ingest_youtube(url)       
    else:
        await ingest_url(url)