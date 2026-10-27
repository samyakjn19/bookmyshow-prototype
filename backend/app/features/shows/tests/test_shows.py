from fastapi.testclient import TestClient


def test_list_shows_empty(client: TestClient) -> None:
    response = client.get("/api/v1/shows")
    assert response.status_code == 200
    assert response.json() == []


def test_create_show_flow(client: TestClient) -> None:
    city = client.post("/api/v1/cities", json={"name": "Mumbai", "slug": "mumbai"}).json()
    movie = client.post("/api/v1/movies", json={"title": "Pathaan", "language": "Hindi"}).json()
    theatre = client.post(
        "/api/v1/theatres", json={"name": "PVR", "city_id": city["id"]}
    ).json()
    show = client.post(
        "/api/v1/shows",
        json={
            "movie_id": movie["id"],
            "theatre_id": theatre["id"],
            "start_at": "2026-11-01T18:00:00",
        },
    )
    assert show.status_code == 201
    assert show.json()["theatre_name"] == "PVR"
