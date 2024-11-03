from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.api import crud
from app.models.tortoise import SummarySchema


router = APIRouter(prefix="/summaries")

@router.post("/")
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    id = await crud.post(payload)

    response_object = {
        "id": id,
        "url": payload.url
    }

    return JSONResponse(
        status_code=201,
        content=response_object
    )

@router.get("/{id}")
async def read_summary(id: int) -> SummarySchema:
    summary = await crud.get(id)

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail="Summary not found"
        )

    return summary

@router.get("/")
async def read_all_summaries() -> List[SummarySchema]:
    return await crud.get_all()