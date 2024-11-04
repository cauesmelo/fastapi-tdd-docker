import logging
import os

from tortoise import Tortoise

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


async def init_db():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["app.models.tortoise"]},
    )

    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


async def init_test_db():
    await Tortoise.init(
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
    )
    await Tortoise._drop_databases()

    await Tortoise.init(
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        _create_db=True,
    )
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


async def clear_test_db():
    await Tortoise._drop_databases()
