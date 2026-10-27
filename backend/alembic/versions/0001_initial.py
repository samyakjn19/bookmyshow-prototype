"""initial tables

Revision ID: 0001
Revises:
Create Date: 2026-10-27
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column("slug", sa.String(100), nullable=False, unique=True),
    )
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("language", sa.String(50), nullable=False),
    )
    op.create_table(
        "theatres",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("city_id", sa.Integer(), sa.ForeignKey("cities.id"), nullable=False),
    )
    op.create_table(
        "shows",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("movie_id", sa.Integer(), sa.ForeignKey("movies.id"), nullable=False),
        sa.Column("theatre_id", sa.Integer(), sa.ForeignKey("theatres.id"), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "seats",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("show_id", sa.Integer(), sa.ForeignKey("shows.id"), nullable=False),
        sa.Column("code", sa.String(10), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="available"),
        sa.UniqueConstraint("show_id", "code", name="uq_show_seat_code"),
    )
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("show_id", sa.Integer(), sa.ForeignKey("shows.id"), nullable=False),
        sa.Column("seats", sa.String(200), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="confirmed"),
    )


def downgrade() -> None:
    op.drop_table("bookings")
    op.drop_table("seats")
    op.drop_table("shows")
    op.drop_table("theatres")
    op.drop_table("movies")
    op.drop_table("cities")
