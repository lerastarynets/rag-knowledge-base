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
# Feedback
# ---------------------------------------------------------------------------


class FeedbackRequest(BaseModel):
    message_id: str
    rating: Literal["up", "down"]
    comment: str | None = None


class FeedbackResponse(BaseModel):
    received: bool


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel):
    status: Literal["ok"]
