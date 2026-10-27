from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.features.movies.models import Movie
from app.features.movies.schemas import MovieCreate, MovieOut
from app.features.shows.models import Show, Theatre


def list_movies(db: Session, city_id: int | None = None) -> list[MovieOut]:
    stmt = select(Movie).order_by(Movie.title)
    if city_id is not None:
        stmt = (
            select(Movie)
            .join(Show, Show.movie_id == Movie.id)
            .join(Theatre, Theatre.id == Show.theatre_id)
            .where(Theatre.city_id == city_id)
            .distinct()
            .order_by(Movie.title)
        )
    rows = db.scalars(stmt).all()
    return [MovieOut.model_validate(row) for row in rows]


def get_movie(db: Session, movie_id: int) -> MovieOut:
    row = db.get(Movie, movie_id)
    if row is None:
        raise NotFoundError("Movie not found")
    return MovieOut.model_validate(row)


def create_movie(db: Session, payload: MovieCreate) -> MovieOut:
    row = Movie(title=payload.title, language=payload.language)
    db.add(row)
    db.commit()
    db.refresh(row)
    return MovieOut.model_validate(row)


def search_movies(db: Session, query: str) -> list[MovieOut]:
    needle = f"%{query.strip().lower()}%"
    rows = db.scalars(
        select(Movie).where(func.lower(Movie.title).like(needle)).order_by(Movie.title)
    ).all()
    return [MovieOut.model_validate(row) for row in rows]
