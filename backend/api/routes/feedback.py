"""Feedback routes: API endpoints for collecting user feedback on responses."""

from __future__ import annotations

from fastapi import APIRouter

from models.schemas import FeedbackRequest, FeedbackResponse

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(body: FeedbackRequest) -> FeedbackResponse:
    # TODO: persist feedback to the database
    return FeedbackResponse(received=True)
