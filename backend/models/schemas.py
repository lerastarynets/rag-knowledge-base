"""Pydantic schemas: request and response models for the API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

# ---------------------------------------------------------------------------
# Ingest
# ---------------------------------------------------------------------------


class IngestUrlRequest(BaseModel):
    url: HttpUrl


class IngestJobResponse(BaseModel):
    """Response after a synchronous ingest completes."""

    job_id: str  # reserved for a future async job queue; placeholder for now
    status: Literal["ok"]


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------


class ChatRequest(BaseModel):
    message: str
    session_id: str = Field(
        description="Reserved for future multi-turn memory; not used by the server yet."
    )


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel):
    status: Literal["ok"]
    url_ingest_enabled: bool
