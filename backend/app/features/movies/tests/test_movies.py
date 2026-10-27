from fastapi.testclient import TestClient


def test_list_movies_empty(client: TestClient) -> None:
    response = client.get("/api/v1/movies")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_search_movie(client: TestClient) -> None:
    created = client.post("/api/v1/movies", json={"title": "Jawan", "language": "Hindi"})
    assert created.status_code == 201
    search = client.get("/api/v1/movies/search", params={"q": "jaw"})
    assert search.status_code == 200
    assert search.json()[0]["title"] == "Jawan"
