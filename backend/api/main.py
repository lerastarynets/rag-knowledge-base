"""Main entry point: initializes and configures the FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import chat, ingest
from config import settings
from constants import FEEDBACK_HEADER_DOWN, FEEDBACK_HEADER_UP
from models.schemas import HealthResponse

app = FastAPI(title="RAG Knowledge Base API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[FEEDBACK_HEADER_UP, FEEDBACK_HEADER_DOWN],
)

app.include_router(ingest.router)
app.include_router(chat.router)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        url_ingest_enabled=settings.ENABLE_URL_INGEST,
    )
