from fastapi import Depends, FastAPI

from app.settings import Settings, get_settings

app = FastAPI()


@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {"ping": "pong!", **settings.model_dump()}
