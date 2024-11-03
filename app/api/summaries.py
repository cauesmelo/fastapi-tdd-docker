from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.api import crud


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