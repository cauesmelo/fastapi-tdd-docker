import json
from datetime import datetime

import pytest

from app.api import crud, summaries


@pytest.fixture(autouse=True)
def patch_summary(monkeypatch):
    def mock_generate_summary(id, url):
        return "Sample Summary"

    monkeypatch.setattr(summaries, "generate_summary", mock_generate_summary)


def test_create_summary(test_app, monkeypatch):
    test_request_payload = {"url": "https://foo.bar/"}
    test_response_payload = {"id": 1, "url": "https://foo.bar/"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(
        "/summaries/",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_summaries_invalid_json(test_app):
    response = test_app.post("/summaries/", content=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "url"],
                "msg": "Field required",
                "input": {},
            }
        ]
    }


def test_read_summary(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "url": "https://foo.bar",
        "summary": "summary",
        "created_at": datetime.now().isoformat(),
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "url": "https://foo.bar",
            "summary": "summary",
            "created_at": datetime.now().isoformat(),
        },
        {
            "id": 2,
            "url": "https://testdrivenn.io",
            "summary": "summary",
            "created_at": datetime.now().isoformat(),
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/summaries/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_summary(test_app, monkeypatch):
    async def mock_get(id):
        return {
            "id": 1,
            "url": "https://foo.bar",
            "summary": "summary",
            "created_at": datetime.now().isoformat(),
        }

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return True

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/summaries/1/")
    assert response.status_code == 204


def test_remove_summary_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return False

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_update_summary(test_app, monkeypatch):
    test_request_payload = {"url": "https://foo.bar", "summary": "updated"}
    test_response_payload = {
        "id": 1,
        "url": "https://foo.bar",
        "summary": "summary",
        "created_at": datetime.now().isoformat(),
    }

    async def mock_put(id, payload):
        return test_response_payload

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(
        "/summaries/1/",
        content=json.dumps(test_request_payload),
    )

    # assert response.status_code == 200
    assert response.json() == test_response_payload


def test_update_summary_incorrect_id(test_app, monkeypatch):
    async def mock_put(id, payload):
        return None

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(
        "/summaries/999/",
        content=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app.put(
        "/summaries/0/",
        content=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"gt": 0},
                "input": "0",
                "loc": ["path", "id"],
                "msg": "Input should be greater than 0",
                "type": "greater_than",
            }
        ]
    }


def test_update_summary_invalid_json(test_app, monkeypatch):
    test_response_payload = {
        "id": 1,
        "url": "https://foo.bar",
        "summary": "summary",
        "created_at": datetime.now().isoformat(),
    }

    async def mock_put(id, payload):
        return test_response_payload

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/summaries/1/", content=json.dumps({}))

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "url"],
                "msg": "Field required",
                "type": "missing",
            },
            {
                "input": {},
                "loc": ["body", "summary"],
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }


def test_update_summary_invalid_keys(test_app_with_db, monkeypatch):
    test_response_payload = {
        "id": 1,
        "url": "https://foo.bar",
        "summary": "summary",
        "created_at": datetime.now().isoformat(),
    }

    async def mock_put(id, payload):
        return test_response_payload

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app_with_db.put(
        "/summaries/1/", content=json.dumps({"url": "https://foo.bar"})
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {"url": "https://foo.bar"},
                "loc": ["body", "summary"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }
