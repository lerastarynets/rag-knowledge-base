"""Search module: performs vector similarity search against the knowledge base."""
from langchain_core.documents import Document
from langchain_cohere import CohereRerank
from pydantic import SecretStr

from config import settings
from services import vector_store

reranker = CohereRerank(
    model="rerank-english-v3.0",
    top_n=5,
    cohere_api_key=SecretStr(settings.COHERE_API_KEY),
)

async def search(query: str) -> list[Document]:
    results = await vector_store.asimilarity_search(query, k=20)
    reranked_results = await reranker.acompress_documents(documents=results, query=query)
    return list(reranked_results)