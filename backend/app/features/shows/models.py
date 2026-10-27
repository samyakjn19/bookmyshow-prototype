from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Theatre(Base):
    __tablename__ = "theatres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))


class Show(Base):
    __tablename__ = "shows"

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    theatre_id: Mapped[int] = mapped_column(ForeignKey("theatres.id"))
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
