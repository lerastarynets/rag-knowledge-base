"""YouTube ingestor: fetches transcripts from YouTube videos for indexing."""
from langchain_community.document_loaders import YoutubeLoader
from pydantic import HttpUrl

async def ingest_youtube(url: HttpUrl):
    loader = YoutubeLoader.from_youtube_url(
        str(url),
        add_video_info=False,
    )
    documents = loader.load()
    print("documents youtube", documents)