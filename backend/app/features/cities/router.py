from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.features.cities.schemas import CityCreate, CityOut
from app.features.cities import service

router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("", response_model=list[CityOut])
def get_cities(db: Session = Depends(get_db)) -> list[CityOut]:
    return service.list_cities(db)


@router.get("/{city_id}", response_model=CityOut)
def get_city(city_id: int, db: Session = Depends(get_db)) -> CityOut:
    return service.get_city(db, city_id)


@router.post("", response_model=CityOut, status_code=201)
def post_city(payload: CityCreate, db: Session = Depends(get_db)) -> CityOut:
    return service.create_city(db, payload)
