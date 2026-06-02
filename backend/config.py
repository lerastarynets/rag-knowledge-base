"""Load application settings from environment variables."""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # OpenAI — embeddings and chat completions
    OPENAI_API_KEY: str

    # Qdrant — vector database
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""  # empty = local instance, fill in = Qdrant Cloud
    QDRANT_COLLECTION_NAME: str = "rag-knowledge-base"

    # Cohere — reranking
    COHERE_API_KEY: str

    # Anthropic — optional alternative LLM
    ANTHROPIC_API_KEY: str = ""

    # LangSmith — LangChain tracing and evaluation
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str = "rag-knowledge-base"
    LANGSMITH_TRACING: str = "true"
    LANGSMITH_ENDPOINT: str = "https://eu.api.smith.langchain.com"


settings = Settings.model_validate({})

os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT
os.environ["LANGSMITH_TRACING"] = settings.LANGSMITH_TRACING
os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
