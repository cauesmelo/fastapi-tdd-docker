from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.api import crud
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema

router = APIRouter(prefix="/summaries")


@router.post("/", response_model=SummaryResponseSchema)
async def create_summary(payload: SummaryPayloadSchema):
    id = await crud.post(payload)

    response_object = {"id": id, "url": payload.url}

    return JSONResponse(status_code=201, content=response_object)


@router.get("/{id}", response_model=SummarySchema)
async def read_summary(id: int):
    summary = await crud.get(id)

    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries() -> List:
    return await crud.get_all()


@router.delete("/{id}")
async def delete_summary(id: int):
    response = await crud.delete(id)

    if response is False:
        raise HTTPException(status_code=404, detail="Summary not found")

    return JSONResponse(status_code=204, content=None)
