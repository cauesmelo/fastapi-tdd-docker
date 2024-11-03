import logging
import os
from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

from app.settings import get_settings

log = logging.getLogger("uvicorn")
settings = get_settings()

TORTOISE_ORM = {
    "connections": {"default": settings.database_url},
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI):
    register_tortoise(
        app=app,
        db_url=settings.database_url,
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )

async def generate_schema():
    log.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=settings.db_url,
        modules={"models": ["models.tortoise"]}
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()

if __name__ == "__main__":
    run_async(generate_schema())
