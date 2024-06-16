from typing import List, Optional
from pydantic import BaseModel, Field

class CharacterSchema(BaseModel):
    name: str
    height: Optional[str] = None
    mass: Optional[str] = None
    hair_color: Optional[str] = None
    skin_color: Optional[str] = None
    eye_color: Optional[str] = None
    birth_year: Optional[str] = None
    gender: Optional[str] = None
    homeworld: Optional[str] = None
    films: List[str] = Field(default_factory=list)
    species: List[str] = Field(default_factory=list)
    starships: List[str] = Field(default_factory=list)
    vehicles: List[str] = Field(default_factory=list)