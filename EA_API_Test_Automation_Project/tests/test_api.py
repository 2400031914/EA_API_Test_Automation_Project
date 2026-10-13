import pytest

def test_health_endpoint_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

@pytest.mark.parametrize("user_id, expected_status", [(1, 200), (2, 200), (999, 404)])
def test_get_user_status(client, user_id, expected_status):
    response = client.get(f"/users/{user_id}")
    assert response.status_code == expected_status

def test_get_user_response_schema(client):
    response = client.get("/users/1")
    body = response.get_json()
    assert response.status_code == 200
    assert set(body.keys()) == {"id", "name", "email"}
    assert isinstance(body["id"], int)
    assert isinstance(body["name"], str)
    assert isinstance(body["email"], str)
    assert "@" in body["email"]

def test_create_user_success(client):
    response = client.post("/users", json={"name": "Indrani", "email": "indrani@example.com"})
    assert response.status_code == 201
    body = response.get_json()
    assert body["id"] > 0
    assert body["name"] == "Indrani"
    assert body["email"] == "indrani@example.com"

@pytest.mark.parametrize("payload", [
    {},
    {"email": "indrani@example.com"},
    {"name": "Indrani"},
    {"name": "   ", "email": "indrani@example.com"},
    {"name": "Indrani", "email": "not-an-email"},
])
def test_create_user_rejects_invalid_payloads(client, payload):
    response = client.post("/users", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_user_rejects_non_json_body(client):
    response = client.post("/users", data="not-json", content_type="text/plain")
    assert response.status_code == 400
    assert response.get_json()["error"] == "invalid_json"
