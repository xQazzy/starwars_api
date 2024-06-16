from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from db.config import Base

class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    birth_year = Column(String)
    eye_color = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    mass = Column(String)
    skin_color = Column(String)
    homeworld = Column(String)
    films = Column(ARRAY(String), default=[])
    species = Column(ARRAY(String), default=[])
    starships = Column(ARRAY(String), default=[])
    vehicles = Column(ARRAY(String), default=[])
