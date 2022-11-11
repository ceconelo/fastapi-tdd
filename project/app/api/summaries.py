from typing import List

from fastapi import APIRouter, HTTPException

from app.api import crud
from app.models.pydantic import (SummaryPayloadSchema,  # isort:skip
                                 SummaryResponseSchema,
                                 SummaryUpdatePayloadSchema)
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema):
    summary_id = await crud.post(payload)
    response_object = {"id": summary_id, "url": payload.url}
    return response_object


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(id: int) -> SummarySchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries() -> List[SummarySchema]:
    summaries = await crud.get_all()
    if not summaries:
        raise HTTPException(status_code=404, detail="No summaries found")
    return summaries


@router.delete("/{id}/", response_model=SummarySchema)
async def remove_summary(id: int) -> SummarySchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    await crud.delete(id)

    return summary


@router.put("/{id}/", response_model=SummarySchema)
async def update_summary(id: int, payload: SummaryUpdatePayloadSchema) -> SummarySchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    updated_summary = await crud.put(id, payload)

    return updated_summary
