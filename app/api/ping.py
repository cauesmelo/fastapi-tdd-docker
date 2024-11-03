from fastapi import APIRouter, Depends

from app.settings import Settings, get_settings

router = APIRouter()


@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {"ping": "pong!", **settings.model_dump()}
