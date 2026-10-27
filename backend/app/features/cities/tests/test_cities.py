from fastapi.testclient import TestClient


def test_list_cities_empty(client: TestClient) -> None:
    response = client.get("/api/v1/cities")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_city(client: TestClient) -> None:
    created = client.post("/api/v1/cities", json={"name": "Delhi", "slug": "delhi"})
    assert created.status_code == 201
    city_id = created.json()["id"]
    fetched = client.get(f"/api/v1/cities/{city_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Delhi"
