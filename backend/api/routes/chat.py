"""Chat routes: API endpoints for querying the RAG knowledge base."""

from __future__ import annotations

import uuid
from typing import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.runnables import RunnableConfig

from chain import RAG_CHAIN
from constants import (
    FEEDBACK_HEADER_DOWN,
    FEEDBACK_HEADER_UP,
    INSUFFICIENT_CONTEXT_MESSAGE,
)
from exceptions import InsufficientContextError
from models.schemas import ChatRequest
from services import langsmith_client

router = APIRouter(prefix="/chat", tags=["chat"])


async def _chat_stream(query: str, run_id: uuid.UUID) -> AsyncGenerator[str, None]:
    # body.session_id is accepted for API compatibility; memory is not implemented yet.
    try:
        async for chunk in RAG_CHAIN.astream(
            {"question": query},
            config=RunnableConfig(run_id=run_id, run_name="chat"),
        ):
            yield chunk
    except InsufficientContextError:
        yield INSUFFICIENT_CONTEXT_MESSAGE


@router.post("/")
async def chat(body: ChatRequest) -> StreamingResponse:
    run_id = uuid.uuid4()
    thumbs_up = langsmith_client.create_presigned_feedback_token(
        run_id, "thumbs_up"
    )
    thumbs_down = langsmith_client.create_presigned_feedback_token(
        run_id, "thumbs_down"
    )
    return StreamingResponse(
        headers={
            FEEDBACK_HEADER_UP: thumbs_up.url,
            FEEDBACK_HEADER_DOWN: thumbs_down.url,
        },
        content=_chat_stream(query=body.message, run_id=run_id),
        media_type="text/plain",
    )
