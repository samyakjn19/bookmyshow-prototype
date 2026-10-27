from fastapi import APIRouter, FastAPI

from app.features.bookings.router import router as bookings_router
from app.features.cities.router import router as cities_router
from app.features.movies.router import router as movies_router
from app.features.shows.router import router as shows_router

health_router = APIRouter(tags=["health"])


@health_router.get("/health")
def health() -> dict:
    return {"status": "ok"}


def register_routers(app: FastAPI) -> None:
    app.include_router(health_router)
    app.include_router(cities_router, prefix="/api/v1")
    app.include_router(movies_router, prefix="/api/v1")
    app.include_router(shows_router, prefix="/api/v1")
    app.include_router(bookings_router, prefix="/api/v1")
