"""Search module: performs vector similarity search against the knowledge base."""

from langchain_core.documents import Document

from services import reranker, vector_store


async def search(query: str) -> list[Document]:
    results = await vector_store.asimilarity_search(query, k=20)
    reranked_results = await reranker.acompress_documents(
        documents=results, query=query
    )
    return list(reranked_results)
