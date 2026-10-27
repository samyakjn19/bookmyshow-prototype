from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.features.shows.schemas import ShowCreate, ShowOut, TheatreCreate, TheatreOut
from app.features.shows import service

router = APIRouter(tags=["shows"])


@router.get("/theatres", response_model=list[TheatreOut])
def get_theatres(
    city_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[TheatreOut]:
    return service.list_theatres(db, city_id=city_id)


@router.post("/theatres", response_model=TheatreOut, status_code=201)
def post_theatre(payload: TheatreCreate, db: Session = Depends(get_db)) -> TheatreOut:
    return service.create_theatre(db, payload)


@router.get("/shows", response_model=list[ShowOut])
def get_shows(
    city_id: int | None = Query(default=None),
    movie_id: int | None = Query(default=None),
    on_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[ShowOut]:
    return service.list_shows(db, city_id=city_id, movie_id=movie_id, on_date=on_date)


@router.get("/shows/{show_id}", response_model=ShowOut)
def get_show(show_id: int, db: Session = Depends(get_db)) -> ShowOut:
    return service.get_show(db, show_id)


@router.post("/shows", response_model=ShowOut, status_code=201)
def post_show(payload: ShowCreate, db: Session = Depends(get_db)) -> ShowOut:
    return service.create_show(db, payload)
