import json


def test_create_summary(test_app_with_db):
    payload = {"url": "https://foo.bar"}

    response = test_app_with_db.post("/summaries/", content=json.dumps(payload))

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_create_summaries_invalid_json(test_app_with_db):
    payload = {}

    response = test_app_with_db.post("/summaries/", content=json.dumps(payload))

    assert response.status_code == 422


def test_read_summary(test_app_with_db):
    # create new
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries/", content=json.dumps(payload))
    id = response.json()["id"]

    # get created
    response = test_app_with_db.get(f"/summaries/{id}/")
    response_dict = response.json()

    assert response.status_code == 200
    assert response_dict["id"] == id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app_with_db.get("/summaries/0/")
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


def test_read_all_summaries(test_app_with_db):
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries", content=json.dumps(payload))

    id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()
    filter_by_id = list(filter(lambda d: d["id"] == id, response_list))
    assert len(filter_by_id) == 1


def test_remove_summary(test_app_with_db):
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries", content=json.dumps(payload))
    id = response.json()["id"]

    response = test_app_with_db.delete(f"/summaries/{id}")

    assert response.status_code == 204


def test_remove_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/summaries/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"
    response = test_app_with_db.delete("/summaries/0/")

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


def test_update_summary(test_app_with_db):
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries", content=json.dumps(payload))
    id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/{id}/",
        content=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )

    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"] == "updated!"
    assert response_dict["created_at"]


def test_update_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.put(
        "/summaries/999/",
        content=json.dumps({"url": "https://foo.bar", "summary": "updated!"}),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"

    response = test_app_with_db.put(
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


def test_update_summary_invalid_json(test_app_with_db):
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries/", content=json.dumps(payload))
    id = response.json()["id"]

    response = test_app_with_db.put(f"/summaries/{id}/", content=json.dumps({}))

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


def test_update_summary_invalid_keys(test_app_with_db):
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries/", content=json.dumps(payload))
    id = response.json()["id"]

    response = test_app_with_db.put(
        f"/summaries/{id}/", content=json.dumps({"url": "https://foo.bar"})
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
