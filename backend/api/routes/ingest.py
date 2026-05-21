"""Ingest routes: API endpoints for uploading and indexing documents."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, UploadFile

from models.schemas import IngestJobResponse, IngestUrlRequest

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/file", response_model=IngestJobResponse)
async def ingest_file(file: UploadFile) -> IngestJobResponse:
    # TODO: pass file to the ingestor pipeline and enqueue a processing job
    job_id = str(uuid.uuid4())
    return IngestJobResponse(job_id=job_id, status="queued")


@router.post("/url", response_model=IngestJobResponse)
async def ingest_url(body: IngestUrlRequest) -> IngestJobResponse:
    # TODO: pass URL to the ingestor pipeline and enqueue a processing job
    job_id = str(uuid.uuid4())
    return IngestJobResponse(job_id=job_id, status="queued")
