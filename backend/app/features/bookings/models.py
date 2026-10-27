from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Seat(Base):
    __tablename__ = "seats"
    __table_args__ = (UniqueConstraint("show_id", "code", name="uq_show_seat_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    show_id: Mapped[int] = mapped_column(ForeignKey("shows.id"))
    code: Mapped[str] = mapped_column(String(10))
    status: Mapped[str] = mapped_column(String(20), default="available")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    show_id: Mapped[int] = mapped_column(ForeignKey("shows.id"))
    seats: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20), default="confirmed")
