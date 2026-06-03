"""Pydantic schemas: request and response models for the API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, HttpUrl

# ---------------------------------------------------------------------------
# Ingest
# ---------------------------------------------------------------------------


class IngestUrlRequest(BaseModel):
    url: HttpUrl


class IngestJobResponse(BaseModel):
    job_id: str
    status: Literal["queued"]


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------


class ChatRequest(BaseModel):
    message: str
    session_id: str


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel):
    status: Literal["ok"]
