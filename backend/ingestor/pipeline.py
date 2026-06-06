"""Ingest documents from various sources."""

import asyncio
import logging

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from services import vector_store

logger = logging.getLogger(__name__)

BATCH_SIZE = 100


async def split_documents(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    return await asyncio.to_thread(text_splitter.split_documents, documents)


async def index_documents(chunks: list[Document]) -> None:
    if not chunks:
        logger.info("VectorStore Indexing: No documents to index")
        return

    logger.info(
        "VectorStore Indexing: Preparing to add %s documents to vector store",
        len(chunks),
    )

    batches = [chunks[i : i + BATCH_SIZE] for i in range(0, len(chunks), BATCH_SIZE)]

    logger.info(
        "VectorStore Indexing: Split into %s batches of %s documents each",
        len(batches),
        BATCH_SIZE,
    )

    async def index_batch(batch: list[Document], batch_num: int) -> bool:
        try:
            await vector_store.aadd_documents(documents=batch)
            logger.info(
                "VectorStore Indexing: Batch %s/%s (%s documents) added successfully",
                batch_num,
                len(batches),
                len(batch),
            )
        except Exception:
            logger.exception(
                "VectorStore Indexing: Error adding batch %s/%s (%s documents)",
                batch_num,
                len(batches),
                len(batch),
            )
            return False
        return True

    tasks = [
        index_batch(batch, batch_num)
        for batch_num, batch in enumerate(batches, start=1)
    ]
    results = await asyncio.gather(*tasks)

    successful = sum(results)

    if successful == len(batches):
        logger.info(
            "VectorStore Indexing: All batches processed successfully! (%s/%s)",
            successful,
            len(batches),
        )
    else:
        logger.warning(
            "VectorStore Indexing: Processed %s/%s batches successfully",
            successful,
            len(batches),
        )


async def ingest_documents(
    documents: list[Document], file_name: str | None = None
) -> None:
    if file_name:
        for document in documents:
            document.metadata["source"] = file_name

    chunks = await split_documents(documents)
    await index_documents(chunks)
