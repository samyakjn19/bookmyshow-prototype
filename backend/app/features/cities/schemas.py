from pydantic import BaseModel, Field


class CityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=1, max_length=100)


class CityOut(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}
