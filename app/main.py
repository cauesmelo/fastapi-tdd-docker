from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from app.api import ping, summaries
from app.db import init_db
from app.settings import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up...")

    await init_db()

    log.info("Database connected.")
    yield

    log.info("Stoppping...")


log = logging.getLogger("uvicorn")


def create_application(*, lifespan = None) -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    application.include_router(ping.router)
    application.include_router(summaries.router)
    return application

app = create_application(lifespan=lifespan)