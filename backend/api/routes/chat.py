"""Chat routes: API endpoints for querying the RAG knowledge base."""

from __future__ import annotations

import uuid
from typing import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.runnables import RunnableConfig

from chain import rag_chain
from exceptions import InsufficientContextError
from models.schemas import ChatRequest
from services import langsmith_client

router = APIRouter(prefix="/chat", tags=["chat"])

INSUFFICIENT_CONTEXT_MESSAGE = (
    "I could not find a confident answer to your question in the provided documents."
)


async def _placeholder_stream(
    query: str, run_id: uuid.UUID
) -> AsyncGenerator[str, None]:
    chain = rag_chain()
    try:
        async for chunk in chain.astream(
            {"question": query}, config=RunnableConfig(run_id=run_id, run_name="chat")
        ):
            yield chunk
    except InsufficientContextError:
        yield INSUFFICIENT_CONTEXT_MESSAGE


@router.post("/")
async def chat(body: ChatRequest) -> StreamingResponse:
    run_id = uuid.uuid4()
    tokens = langsmith_client.create_presigned_feedback_tokens(
        run_id,
        feedback_keys=["thumbs_up", "thumbs_down"],
    )
    return StreamingResponse(
        headers={
            "X-Feedback-Up": tokens[0].url,
            "X-Feedback-Down": tokens[1].url,
        },
        content=_placeholder_stream(query=body.message, run_id=run_id),
        media_type="text/plain",
    )
