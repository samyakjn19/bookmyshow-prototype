from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.features.bookings.models import Booking, Seat
from app.features.bookings.schemas import BookingCreate, BookingOut, SeatCreate, SeatOut
from app.features.shows.models import Show
from app.integrations.notifications.service import send as notify


def _booking_out(row: Booking) -> BookingOut:
    return BookingOut(
        id=row.id,
        show_id=row.show_id,
        seats=[code for code in row.seats.split(",") if code],
        status=row.status,
    )


def list_seats(db: Session, show_id: int) -> list[SeatOut]:
    if db.get(Show, show_id) is None:
        raise NotFoundError("Show not found")
    rows = db.scalars(select(Seat).where(Seat.show_id == show_id).order_by(Seat.code)).all()
    return [SeatOut.model_validate(row) for row in rows]


def add_seats(db: Session, show_id: int, payload: SeatCreate) -> list[SeatOut]:
    if db.get(Show, show_id) is None:
        raise NotFoundError("Show not found")
    created: list[Seat] = []
    for code in payload.codes:
        exists = db.scalar(select(Seat).where(Seat.show_id == show_id, Seat.code == code))
        if exists:
            raise ConflictError(f"Seat {code} already exists")
        row = Seat(show_id=show_id, code=code.upper(), status="available")
        db.add(row)
        created.append(row)
    db.commit()
    for row in created:
        db.refresh(row)
    return [SeatOut.model_validate(row) for row in created]


def list_bookings(db: Session) -> list[BookingOut]:
    rows = db.scalars(select(Booking).order_by(Booking.id)).all()
    return [_booking_out(row) for row in rows]


def get_booking(db: Session, booking_id: int) -> BookingOut:
    row = db.get(Booking, booking_id)
    if row is None:
        raise NotFoundError("Booking not found")
    return _booking_out(row)


def create_booking(db: Session, payload: BookingCreate) -> BookingOut:
    if db.get(Show, payload.show_id) is None:
        raise NotFoundError("Show not found")
    codes = [code.strip().upper() for code in payload.seats]
    seats = db.scalars(
        select(Seat).where(Seat.show_id == payload.show_id, Seat.code.in_(codes))
    ).all()
    found = {seat.code: seat for seat in seats}
    missing = [code for code in codes if code not in found]
    if missing:
        raise NotFoundError(f"Seats not found: {', '.join(missing)}")
    taken = [seat.code for seat in seats if seat.status != "available"]
    if taken:
        raise ConflictError(f"Seats already booked: {', '.join(taken)}")
    for seat in seats:
        seat.status = "booked"
    row = Booking(show_id=payload.show_id, seats=",".join(codes), status="confirmed")
    db.add(row)
    db.commit()
    db.refresh(row)
    notify("user", f"Booking {row.id} confirmed for seats {','.join(codes)}")
    return _booking_out(row)
