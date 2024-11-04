from typing import List

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary


async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(url=payload.url, summary="dummy summary")

    await summary.save()
    return summary.id


async def get(id: int) -> dict | None:
    summary = await TextSummary.filter(id=id).first().values()

    if summary:
        return summary

    return None


async def get_all() -> List:
    summaries = await TextSummary.all().values()
    return summaries


async def delete(id: int) -> bool:
    summary = await TextSummary.filter(id=id).first().delete()

    return summary != 0


async def put(id: int, payload: SummaryPayloadSchema):
    summary = await TextSummary.filter(id=id).update(
        url=payload.url, summary=payload.summary
    )

    if summary:
        updated_summary = await TextSummary.filter(id=id).first().values()
        return updated_summary

    return None
