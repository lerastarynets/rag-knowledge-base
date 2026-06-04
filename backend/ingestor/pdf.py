"""PDF ingestor: loads and parses PDF files into text chunks for indexing."""

import asyncio
import logging

from langchain_community.document_loaders import PyPDFLoader

from ingestor.pipeline import ingest_documents

logger = logging.getLogger(__name__)


async def ingest_pdf(file_path: str, file_name: str) -> None:
    loader = PyPDFLoader(file_path=file_path)
    documents = await asyncio.to_thread(loader.load)
    logger.info("ingesting pdf")
    for document in documents:
        document.metadata["source_type"] = "pdf"
    await ingest_documents(documents, file_name)
    logger.info("pdf ingested")
