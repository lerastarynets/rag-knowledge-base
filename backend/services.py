from langchain_cohere import CohereRerank
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langsmith import Client
from pydantic import SecretStr
from qdrant_client import QdrantClient

from config import settings

reranker = CohereRerank(
    model="rerank-english-v3.0",
    top_n=5,
    cohere_api_key=SecretStr(settings.COHERE_API_KEY),
)

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

langsmith_client = Client()
