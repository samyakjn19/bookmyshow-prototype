from fastapi.testclient import TestClient


def _setup_show(client: TestClient) -> int:
    city = client.post("/api/v1/cities", json={"name": "Pune", "slug": "pune"}).json()
    movie = client.post("/api/v1/movies", json={"title": "Dunki", "language": "Hindi"}).json()
    theatre = client.post(
        "/api/v1/theatres", json={"name": "INOX", "city_id": city["id"]}
    ).json()
    show = client.post(
        "/api/v1/shows",
        json={
            "movie_id": movie["id"],
            "theatre_id": theatre["id"],
            "start_at": "2026-11-02T20:00:00",
        },
    ).json()
    return show["id"]


def test_list_bookings_empty(client: TestClient) -> None:
    response = client.get("/api/v1/bookings")
    assert response.status_code == 200
    assert response.json() == []


def test_booking_and_double_book(client: TestClient) -> None:
    show_id = _setup_show(client)
    seats = client.post(f"/api/v1/shows/{show_id}/seats", json={"codes": ["A1", "A2"]})
    assert seats.status_code == 201
    first = client.post("/api/v1/bookings", json={"show_id": show_id, "seats": ["A1"]})
    assert first.status_code == 201
    second = client.post("/api/v1/bookings", json={"show_id": show_id, "seats": ["A1"]})
    assert second.status_code == 409
