import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

# --- Setup test DB ---
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture
def polygon_data():
    return {
        "name": "TestPolygon",
        "points": [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
    }

# --- Tests ---
@pytest.mark.api
def test_create_polygon(polygon_data):
    response = client.post("/api/polygon/", json=polygon_data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == polygon_data["name"]
    assert result["points"] == polygon_data["points"]
    global polygon_id
    polygon_id = result["id"]

@pytest.mark.api
def test_fetch_polygons():
    response = client.get("/api/polygons/")
    assert response.status_code == 200
    polygons = response.json()
    assert any(p["id"] == polygon_id for p in polygons)

@pytest.mark.api
def test_delete_polygon():
    response = client.delete(f"/api/polygon/{polygon_id}")
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    # Verify deletion
    response = client.get("/api/polygons/")
    polygons = response.json()
    assert all(p["id"] != polygon_id for p in polygons)
