import json

def test_create_summary(test_app_with_db):
    payload = {
        "url": "https://foo.bar"
    }
    
    response = test_app_with_db.post("/summaries/", data=json.dumps(payload))

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"

def test_create_summaries_invalid_json(test_app_with_db):
    payload = {} # empty

    response = test_app_with_db.post("/summaries/", data=json.dumps(payload))

    assert response.status_code == 422