# BookMyShow Prototype

Movie booking API: pick a city, see movies and shows, lock seats, confirm a booking.

## Stack

- FastAPI
- PostgreSQL (Docker Compose)
- Redis and Elasticsearch are wired as optional compose services
- Frontend folder is reserved for a React app

## Run

```powershell
docker compose up -d db
cd backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
$env:PYTHONPATH = (Get-Location)
.\.venv\Scripts\alembic.exe upgrade head
.\.venv\Scripts\uvicorn.exe app.main:app --reload
```

API docs: `http://localhost:8000/docs`

From the repo root you can also use `.\scripts\start.ps1`.

## API

| Method | Path |
|---|---|
| GET | `/health` |
| GET, POST | `/api/v1/cities` |
| GET | `/api/v1/cities/{id}` |
| GET, POST | `/api/v1/movies` |
| GET | `/api/v1/movies/search?q=` |
| GET, POST | `/api/v1/theatres` |
| GET, POST | `/api/v1/shows` |
| GET, POST | `/api/v1/shows/{id}/seats` |
| GET, POST | `/api/v1/bookings` |

Add rows with POST, or with `backend/app/db/seeds` when you fill it in.

## Tests

```powershell
.\scripts\test.ps1
```
