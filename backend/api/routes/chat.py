"""Chat routes: API endpoints for querying the RAG knowledge base."""

from __future__ import annotations

from typing import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from chain import rag_chain
from exceptions import InsufficientContextError
from models.schemas import ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])

INSUFFICIENT_CONTEXT_MESSAGE = (
    "I could not find a confident answer to your question "
    "in the provided documents."
)


async def _placeholder_stream(query: str) -> AsyncGenerator[str, None]:
    chain = rag_chain()
    try:
        async for chunk in chain.astream({"question": query}):
            yield chunk
    except InsufficientContextError:
        yield INSUFFICIENT_CONTEXT_MESSAGE


@router.post("/")
async def chat(body: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        _placeholder_stream(query=body.message), media_type="text/plain"
    )
