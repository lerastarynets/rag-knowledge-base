from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from config import settings
from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=SecretStr(settings.OPENAI_API_KEY),
)

vector_store = QdrantVectorStore(
    client=QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY or None),
    collection_name=settings.QDRANT_COLLECTION_NAME,
    embedding=embeddings,
)