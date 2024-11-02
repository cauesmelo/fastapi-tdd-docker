from fastapi import Depends, FastAPI
from tortoise import Tortoise

from app.settings import Settings, get_settings
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

settings = get_settings()

async def init():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )

    await Tortoise.generate_schemas()

@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {"ping": "pong!", **settings.model_dump()}
