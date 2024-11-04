from typing import List

from fastapi import APIRouter, BackgroundTasks, HTTPException, Path
from fastapi.responses import JSONResponse

from app.api import crud
from app.models.tortoise import SummarySchema
from app.summarizer import generate_summary

from app.models.pydantic import (  # isort:skip
    SummaryPayloadSchema,
    SummaryResponseSchema,
    SummaryUpdatePayloadSchema,
)

router = APIRouter(prefix="/summaries")


@router.post("/", response_model=SummaryResponseSchema)
async def create_summary(
    payload: SummaryPayloadSchema, background_tasks: BackgroundTasks
):
    id = await crud.post(payload)

    background_tasks.add_task(generate_summary, id, str(payload.url))

    response_object = {"id": id, "url": payload.url}

    return JSONResponse(status_code=201, content=response_object)


@router.get("/{id}", response_model=SummarySchema)
async def read_summary(id: int = Path(..., gt=0)):
    summary = await crud.get(id)

    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries() -> List:
    return await crud.get_all()


@router.delete("/{id}")
async def delete_summary(id: int = Path(..., gt=0)):
    response = await crud.delete(id)

    if response is False:
        raise HTTPException(status_code=404, detail="Summary not found")

    return JSONResponse(status_code=204, content=None)


@router.put("/{id}")
async def update_summary(
    payload: SummaryUpdatePayloadSchema, id: int = Path(..., gt=0)
):
    summary = await crud.put(id, payload)

    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary
