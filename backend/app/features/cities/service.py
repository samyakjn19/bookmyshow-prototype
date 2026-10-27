from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.features.cities.models import City
from app.features.cities.schemas import CityCreate, CityOut


def list_cities(db: Session) -> list[CityOut]:
    rows = db.scalars(select(City).order_by(City.name)).all()
    return [CityOut.model_validate(row) for row in rows]


def get_city(db: Session, city_id: int) -> CityOut:
    row = db.get(City, city_id)
    if row is None:
        raise NotFoundError("City not found")
    return CityOut.model_validate(row)


def create_city(db: Session, payload: CityCreate) -> CityOut:
    exists = db.scalar(select(City).where((City.slug == payload.slug) | (City.name == payload.name)))
    if exists:
        raise ConflictError("City already exists")
    row = City(name=payload.name, slug=payload.slug)
    db.add(row)
    db.commit()
    db.refresh(row)
    return CityOut.model_validate(row)
