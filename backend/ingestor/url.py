"""URL ingestor: fetches and parses web pages into text chunks for indexing."""
from langchain_community.document_loaders import WebBaseLoader
from pydantic import HttpUrl
from ingestor.pipeline import ingest_documents

async def ingest_url(url: HttpUrl):
    loader = WebBaseLoader(web_paths=[str(url)])
    documents = loader.load()
    print("ingesting url")
    ingest_documents(documents)
    print("url ingested")