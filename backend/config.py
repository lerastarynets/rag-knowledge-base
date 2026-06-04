"""Load application settings from environment variables."""

from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).resolve().parent / ".env"

# Populate os.environ so LangSmith (and other SDKs) read vars from backend/.env.
load_dotenv(_ENV_FILE)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # OpenAI — embeddings and chat completions
    OPENAI_API_KEY: str

    # Qdrant — vector database
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""  # empty = local instance, fill in = Qdrant Cloud
    QDRANT_COLLECTION_NAME: str

    # Cohere — reranking
    COHERE_API_KEY: str

    # Anthropic — optional alternative LLM
    ANTHROPIC_API_KEY: str = ""


settings = Settings()
