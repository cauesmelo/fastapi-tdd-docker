from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
import pytest
from starlette.testclient import TestClient
from app.db import clear_test_db, init_test_db
from app.main import create_application
from app.settings import get_settings, Settings


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@asynccontextmanager
async def test_lifespan(app: FastAPI):
    await init_test_db()

    yield

    await clear_test_db()


@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_application(lifespan=test_lifespan)
    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down
