from fastapi import APIRouter, Depends

from app.settings import get_settings, Settings

router = APIRouter()

@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {"ping": "pong!", **settings.model_dump()}
