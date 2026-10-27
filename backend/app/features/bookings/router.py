from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.features.bookings.schemas import BookingCreate, BookingOut, SeatCreate, SeatOut
from app.features.bookings import service

router = APIRouter(tags=["bookings"])


@router.get("/shows/{show_id}/seats", response_model=list[SeatOut])
def get_seats(show_id: int, db: Session = Depends(get_db)) -> list[SeatOut]:
    return service.list_seats(db, show_id)


@router.post("/shows/{show_id}/seats", response_model=list[SeatOut], status_code=201)
def post_seats(
    show_id: int, payload: SeatCreate, db: Session = Depends(get_db)
) -> list[SeatOut]:
    return service.add_seats(db, show_id, payload)


@router.get("/bookings", response_model=list[BookingOut])
def get_bookings(db: Session = Depends(get_db)) -> list[BookingOut]:
    return service.list_bookings(db)


@router.get("/bookings/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int, db: Session = Depends(get_db)) -> BookingOut:
    return service.get_booking(db, booking_id)


@router.post("/bookings", response_model=BookingOut, status_code=201)
def post_booking(payload: BookingCreate, db: Session = Depends(get_db)) -> BookingOut:
    return service.create_booking(db, payload)
