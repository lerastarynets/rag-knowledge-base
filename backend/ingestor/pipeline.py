"""Ingestor pipeline: ingests documents from various sources and enqueues a processing job."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from pydantic import SecretStr

from config import settings


def ingest_documents(documents: list[Document]) -> None:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=SecretStr(settings.OPENAI_API_KEY),
    )
    QdrantVectorStore.from_documents(
        documents=texts,
        embedding=embeddings,
        collection_name=settings.QDRANT_COLLECTION_NAME,
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
    )