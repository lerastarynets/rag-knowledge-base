"""Chat routes: API endpoints for querying the RAG knowledge base."""

from __future__ import annotations

import asyncio
from typing import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models.schemas import ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])


async def _placeholder_stream() -> AsyncGenerator[str, None]:
    # TODO: replace with actual RAG chain streaming output
    for chunk in ["placeholder", " ", "response"]:
        yield chunk
        await asyncio.sleep(0)


@router.post("/")
async def chat(body: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        _placeholder_stream(),
        media_type="text/plain",
    )
