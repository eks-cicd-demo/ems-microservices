from app import app


def test_health_endpoint():
    """
    Verify the dashboard service health endpoint.
    """
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["service"] == "dashboard"
    assert data["ok"] is True


def test_stats_requires_auth():
    """
    Verify dashboard stats endpoint requires authentication.
    """
    client = app.test_client()

    response = client.get("/stats")

    assert response.status_code == 401

    data = response.get_json()

    assert "error" in data


def test_unknown_endpoint():
    """
    Verify unknown endpoints return 404.
    """
    client = app.test_client()

    response = client.get("/does-not-exist")

    assert response.status_code == 404