import json


def test_create_summary(test_app_with_db):
    payload = {
        "url": "https://foo.bar"
    }

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
    response = test_app_with_db.get("/summaries/999")

    assert response.status_code == 404


def test_read_all_summaries(test_app_with_db):
    payload = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries", content=json.dumps(payload))

    id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()
    filter_by_id = list(filter(lambda d: d["id"] == id, response_list))
    assert len(filter_by_id) == 1
