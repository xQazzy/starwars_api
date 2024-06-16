import pytest
from schemas.character import CharacterSchema

@pytest.fixture
def character_data():
    return {
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male",
        "homeworld": "Tatooine",
        "films": ["A New Hope", "The Empire Strikes Back", "Return of the Jedi"],
        "species": [],
        "starships": ["X-wing", "Imperial shuttle"],
        "vehicles": ["Snowspeeder", "Imperial speeder bike"]
    }

def test_character_schema(character_data):
    character = CharacterSchema(**character_data)
    assert character.name == character_data['name']
    assert character.height == character_data['height']
    assert character.mass == character_data['mass']
    assert character.hair_color == character_data['hair_color']
    assert character.skin_color == character_data['skin_color']
    assert character.eye_color == character_data['eye_color']
    assert character.birth_year == character_data['birth_year']
    assert character.gender == character_data['gender']
    assert character.homeworld == character_data['homeworld']
    assert character.films == character_data['films']
    assert character.species == character_data['species']
    assert character.starships == character_data['starships']
    assert character.vehicles == character_data['vehicles']

def test_character_schema_default_values():
    character = CharacterSchema(name="Yoda")
    assert character.name == "Yoda"
    assert character.height is None
    assert character.mass is None
    assert character.hair_color is None
    assert character.skin_color is None
    assert character.eye_color is None
    assert character.birth_year is None
    assert character.gender is None
    assert character.homeworld is None
    assert character.films == []
    assert character.species == []
    assert character.starships == []
    assert character.vehicles == []

def test_character_schema_invalid_data():
    with pytest.raises(ValueError):
        CharacterSchema(name=None)