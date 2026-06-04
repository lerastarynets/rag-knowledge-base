"""DOCX ingestor: loads and parses Word documents into text chunks for indexing."""

import asyncio
import logging

from langchain_community.document_loaders import Docx2txtLoader

from ingestor.pipeline import ingest_documents

logger = logging.getLogger(__name__)


async def ingest_docx(file_path: str, file_name: str) -> None:
    loader = Docx2txtLoader(file_path=file_path)
    documents = await asyncio.to_thread(loader.load)
    logger.info("ingesting docx")
    for document in documents:
        document.metadata["source_type"] = "docx"
    await ingest_documents(documents, file_name)
    logger.info("docx ingested")
