"""Ingest documents from various sources and enqueue processing jobs."""

import asyncio
from typing import Optional

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from services import vector_store

BATCH_SIZE = 100


async def split_documents(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    return await asyncio.to_thread(text_splitter.split_documents, documents)


async def index_documents(chunks: list[Document]) -> None:
    if not chunks:
        print("VectorStore Indexing: No documents to index")
        return

    print(
        f"VectorStore Indexing: Preparing to add {len(chunks)} documents "
        "to vector store"
    )

    batches = [chunks[i : i + BATCH_SIZE] for i in range(0, len(chunks), BATCH_SIZE)]

    print(
        f"VectorStore Indexing: Split into {len(batches)} batches "
        f"of {BATCH_SIZE} documents each"
    )

    async def index_batch(batch: list[Document], batch_num: int) -> bool:
        try:
            await vector_store.aadd_documents(documents=batch)
            print(
                f"VectorStore Indexing: Batch {batch_num}/{len(batches)} "
                f"({len(batch)} documents) added successfully"
            )
        except Exception as e:
            print(
                f"VectorStore Indexing: Error adding batch "
                f"{batch_num}/{len(batches)} ({len(batch)} documents): {e}"
            )
            return False
        return True

    tasks = [
        index_batch(batch, batch_num)
        for batch_num, batch in enumerate(batches, start=1)
    ]
    results = await asyncio.gather(*tasks)

    successful = sum(1 for result in results if result is True)

    if successful == len(batches):
        print(
            f"VectorStore Indexing: All batches processed successfully! "
            f"({successful}/{len(batches)})"
        )
    else:
        print(
            f"VectorStore Indexing: Processed {successful}/{len(batches)} "
            "batches successfully"
        )


async def ingest_documents(
    documents: list[Document], file_name: Optional[str] = None
) -> None:
    if file_name:
        for document in documents:
            document.metadata["source"] = file_name

    chunks = await split_documents(documents)
    await index_documents(chunks)
