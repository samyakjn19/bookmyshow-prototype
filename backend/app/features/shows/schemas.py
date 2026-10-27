from datetime import datetime

from pydantic import BaseModel, Field


class TheatreCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    city_id: int


class TheatreOut(BaseModel):
    id: int
    name: str
    city_id: int

    model_config = {"from_attributes": True}


class ShowCreate(BaseModel):
    movie_id: int
    theatre_id: int
    start_at: datetime


class ShowOut(BaseModel):
    id: int
    movie_id: int
    theatre_id: int
    theatre_name: str
    city_id: int
    start_at: datetime
