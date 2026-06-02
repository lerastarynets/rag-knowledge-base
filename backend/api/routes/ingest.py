"""Ingest routes: API endpoints for uploading and indexing documents."""

from __future__ import annotations

import tempfile
import uuid

from fastapi import APIRouter, HTTPException, UploadFile

from exceptions import IngestionError
from ingestor import file_dispatcher, url_dispatcher
from models.schemas import IngestJobResponse, IngestUrlRequest

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/file", response_model=IngestJobResponse)
async def ingest_file_route(file: UploadFile) -> IngestJobResponse:
    # TODO: pass file to the ingestor pipeline and enqueue a processing job
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        # 2. Write the uploaded file content to the temp file
        tmp.write(await file.read())
        tmp.flush()
        await file_dispatcher(
            file_path=tmp.name,
            file_name=file.filename or "",
            file_content_type=file.content_type or "",
        )
    job_id = str(uuid.uuid4())
    return IngestJobResponse(job_id=job_id, status="queued")


@router.post("/url", response_model=IngestJobResponse)
async def ingest_url_route(body: IngestUrlRequest) -> IngestJobResponse:
    # TODO: pass URL to the ingestor pipeline and enqueue a processing job
    try:
        await url_dispatcher(body.url)
    except IngestionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    job_id = str(uuid.uuid4())
    return IngestJobResponse(job_id=job_id, status="queued")
