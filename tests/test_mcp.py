from fastapi.testclient import TestClient
from backend.mcp_server import app

client = TestClient(app)


def test_list_sources():
    response = client.get("/sources")
    assert response.status_code == 200
    data = response.json()
    assert "sources" in data
    assert len(data["sources"]) >= 2


def test_search_endpoint():
    response = client.get("/search?q=country")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    assert results[0]["column"] == "country"


def test_search_empty():
    response = client.get("/search?q=")
    assert response.status_code == 200
    assert response.json() == []


def test_get_schema():
    response = client.get("/schema/main_db/users")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "users"
    assert len(data["columns"]) > 0


def test_get_schema_not_found():
    response = client.get("/schema/unknown/unknown")
    assert response.status_code == 200
    assert "error" in response.json()


def test_index():
    response = client.post("/index")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

