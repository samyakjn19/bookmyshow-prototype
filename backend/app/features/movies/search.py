from sqlalchemy.orm import Session

from app.features.movies.schemas import MovieOut
from app.features.movies.service import search_movies as postgres_search


def search_movies(db: Session, query: str) -> list[MovieOut]:
    return postgres_search(db, query)
