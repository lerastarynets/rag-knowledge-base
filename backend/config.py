"""Configuration module: loads and exposes application settings from environment variables."""

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
    QDRANT_API_KEY: str = ""          # empty = local instance, fill in = Qdrant Cloud
    QDRANT_COLLECTION_NAME: str = "rag-knowledge-base"

    # Cohere — reranking
    COHERE_API_KEY: str

    # Anthropic — optional alternative LLM
    ANTHROPIC_API_KEY: str = ""

    # LangSmith — LangChain tracing and evaluation
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str = "rag-knowledge-base"
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"


settings = Settings.model_validate({})
