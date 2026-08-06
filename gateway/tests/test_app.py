from app import app


def test_root_endpoint():
    """
    Verify the gateway home page loads successfully.
    """
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_health_endpoint():
    """
    Verify the gateway health endpoint is available.
    """
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["service"] == "gateway"
    assert data["ok"] is True

    assert "services" in data
    assert isinstance(data["services"], dict)


def test_invalid_endpoint():
    """
    Verify an unknown endpoint returns HTTP 404.
    """
    client = app.test_client()

    response = client.get("/invalid-url")

    assert response.status_code == 404