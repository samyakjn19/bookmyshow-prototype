from pydantic import BaseModel, Field


class SeatOut(BaseModel):
    id: int
    show_id: int
    code: str
    status: str

    model_config = {"from_attributes": True}


class SeatCreate(BaseModel):
    codes: list[str] = Field(min_length=1)


class BookingCreate(BaseModel):
    show_id: int
    seats: list[str] = Field(min_length=1)


class BookingOut(BaseModel):
    id: int
    show_id: int
    seats: list[str]
    status: str
