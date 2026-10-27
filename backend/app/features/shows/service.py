from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.features.cities.models import City
from app.features.movies.models import Movie
from app.features.shows.models import Show, Theatre
from app.features.shows.schemas import ShowCreate, ShowOut, TheatreCreate, TheatreOut


def list_theatres(db: Session, city_id: int | None = None) -> list[TheatreOut]:
    stmt = select(Theatre).order_by(Theatre.name)
    if city_id is not None:
        stmt = stmt.where(Theatre.city_id == city_id)
    rows = db.scalars(stmt).all()
    return [TheatreOut.model_validate(row) for row in rows]


def create_theatre(db: Session, payload: TheatreCreate) -> TheatreOut:
    if db.get(City, payload.city_id) is None:
        raise NotFoundError("City not found")
    row = Theatre(name=payload.name, city_id=payload.city_id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return TheatreOut.model_validate(row)


def _to_show_out(show: Show, theatre: Theatre) -> ShowOut:
    return ShowOut(
        id=show.id,
        movie_id=show.movie_id,
        theatre_id=show.theatre_id,
        theatre_name=theatre.name,
        city_id=theatre.city_id,
        start_at=show.start_at,
    )


def list_shows(
    db: Session,
    city_id: int | None = None,
    movie_id: int | None = None,
    on_date: date | None = None,
) -> list[ShowOut]:
    stmt = select(Show, Theatre).join(Theatre, Theatre.id == Show.theatre_id)
    if city_id is not None:
        stmt = stmt.where(Theatre.city_id == city_id)
    if movie_id is not None:
        stmt = stmt.where(Show.movie_id == movie_id)
    if on_date is not None:
        start = datetime.combine(on_date, datetime.min.time())
        end = datetime.combine(on_date, datetime.max.time())
        stmt = stmt.where(Show.start_at >= start, Show.start_at <= end)
    stmt = stmt.order_by(Show.start_at)
    rows = db.execute(stmt).all()
    return [_to_show_out(show, theatre) for show, theatre in rows]


def get_show(db: Session, show_id: int) -> ShowOut:
    row = db.execute(
        select(Show, Theatre).join(Theatre, Theatre.id == Show.theatre_id).where(Show.id == show_id)
    ).first()
    if row is None:
        raise NotFoundError("Show not found")
    show, theatre = row
    return _to_show_out(show, theatre)


def create_show(db: Session, payload: ShowCreate) -> ShowOut:
    if db.get(Movie, payload.movie_id) is None:
        raise NotFoundError("Movie not found")
    theatre = db.get(Theatre, payload.theatre_id)
    if theatre is None:
        raise NotFoundError("Theatre not found")
    row = Show(
        movie_id=payload.movie_id,
        theatre_id=payload.theatre_id,
        start_at=payload.start_at,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _to_show_out(row, theatre)
