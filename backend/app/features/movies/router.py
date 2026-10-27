from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.features.movies.schemas import MovieCreate, MovieOut
from app.features.movies import search as movie_search
from app.features.movies import service

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("", response_model=list[MovieOut])
def get_movies(
    city_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[MovieOut]:
    return service.list_movies(db, city_id=city_id)


@router.get("/search", response_model=list[MovieOut])
def search_movies(
    q: str = Query(min_length=1),
    db: Session = Depends(get_db),
) -> list[MovieOut]:
    return movie_search.search_movies(db, q)


@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)) -> MovieOut:
    return service.get_movie(db, movie_id)


@router.post("", response_model=MovieOut, status_code=201)
def post_movie(payload: MovieCreate, db: Session = Depends(get_db)) -> MovieOut:
    return service.create_movie(db, payload)
