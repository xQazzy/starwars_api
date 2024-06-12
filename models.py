from pydantic import BaseModel, Field
from typing import List

class Character(BaseModel):
    id: int
    birth_year: str = Field(default="")
    eye_color: str = Field(default="")
    films: List[str] = Field(default=[])
    gender: str = Field(default="")
    hair_color: str = Field(default="")
    height: str = Field(default="")
    homeworld: str = Field(default="")
    mass: str = Field(default="")
    name: str
    skin_color: str = Field(default="")
    species: List[str] = Field(default=[])
    starships: List[str] = Field(default=[])
    vehicles: List[str] = Field(default=[])
