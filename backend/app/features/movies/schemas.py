from pydantic import BaseModel, Field


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    language: str = Field(min_length=1, max_length=50)


class MovieOut(BaseModel):
    id: int
    title: str
    language: str

    model_config = {"from_attributes": True}
