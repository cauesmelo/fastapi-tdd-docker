def test_ping(test_app):
    # Given
    # test_app

    # When
    response = test_app.get("/ping")

    # Then
    assert response.status_code == 200
    assert response.json() == {
            "environment": "DEV",
            "ping": "pong!",
            "testing": True,
            'database_url': 'postgres://postgres:postgres@db:5432/web_test'
        }
