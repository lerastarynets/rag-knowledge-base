from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from pydantic import SecretStr
from qdrant_client import QdrantClient

from config import settings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=SecretStr(settings.OPENAI_API_KEY),
)

vector_store = QdrantVectorStore(
    client=QdrantClient(
        url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY or None
    ),
    collection_name=settings.QDRANT_COLLECTION_NAME,
    embedding=embeddings,
)

llm = ChatOpenAI(
    model="gpt-5.4-mini", temperature=0, api_key=SecretStr(settings.OPENAI_API_KEY)
)
