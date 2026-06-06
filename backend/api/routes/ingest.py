"""Ingest routes: API endpoints for uploading and indexing documents."""

from __future__ import annotations

import tempfile
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from exceptions import IngestionError, UnsupportedFileTypeError
from ingestor import file_dispatcher, url_dispatcher
from models.schemas import IngestJobResponse, IngestUrlRequest

router = APIRouter(prefix="/ingest", tags=["ingest"])

MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # 50 MiB


@router.post("/file", response_model=IngestJobResponse)
async def ingest_file_route(file: UploadFile) -> IngestJobResponse:
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum size of {MAX_UPLOAD_BYTES} bytes",
        )

    suffix = Path(file.filename or "").suffix or None
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix=suffix) as tmp:
            tmp.write(content)
            tmp.flush()
            await file_dispatcher(
                file_path=tmp.name,
                file_name=file.filename or "",
                file_content_type=file.content_type or "",
            )
    except UnsupportedFileTypeError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    except IngestionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    job_id = str(uuid.uuid4())
    return IngestJobResponse(job_id=job_id, status="ok")


@router.post("/url", response_model=IngestJobResponse)
async def ingest_url_route(body: IngestUrlRequest) -> IngestJobResponse:
    try:
        await url_dispatcher(body.url)
    except IngestionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    job_id = str(uuid.uuid4())
    return IngestJobResponse(job_id=job_id, status="ok")
