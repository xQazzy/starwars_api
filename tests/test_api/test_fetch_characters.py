import pytest
import aiohttp
from aioresponses import aioresponses
from api.fetch_characters import fetch_characters, process_character

@pytest.fixture
async def session():
    async with aiohttp.ClientSession() as session:
        yield session

@pytest.mark.asyncio
async def test_fetch_characters(session):
    with aioresponses() as m:
        m.get("https://swapi.dev/api/people/", payload={
            "results": [
                {
                    "name": "Luke Skywalker",
                    "height": "172",
                    "mass": "77",
                    "hair_color": "blond",
                    "skin_color": "fair",
                    "eye_color": "blue",
                    "birth_year": "19BBY",
                    "gender": "male",
                    "homeworld": "https://swapi.dev/api/planets/1/",
                    "films": ["https://swapi.dev/api/films/1/"],
                    "species": [],
                    "starships": ["https://swapi.dev/api/starships/12/"],
                    "vehicles": ["https://swapi.dev/api/vehicles/14/"]
                }
            ],
            "next": None
        })

        m.get("https://swapi.dev/api/planets/1/", payload={"name": "Tatooine"})
        m.get("https://swapi.dev/api/films/1/", payload={"title": "A New Hope"})
        m.get("https://swapi.dev/api/starships/12/", payload={"name": "X-wing"})
        m.get("https://swapi.dev/api/vehicles/14/", payload={"name": "Snowspeeder"})

        characters = await fetch_characters(session)
        
        assert len(characters) == 1
        assert characters[0]['name'] == "Luke Skywalker"
        assert characters[0]['homeworld'] == "Tatooine"
        assert characters[0]['films'] == ["A New Hope"]
        assert characters[0]['starships'] == ["X-wing"]
        assert characters[0]['vehicles'] == ["Snowspeeder"]

@pytest.mark.asyncio
async def test_process_character(session):
    item = {
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male",
        "homeworld": "https://swapi.dev/api/planets/1/",
        "films": ["https://swapi.dev/api/films/1/"],
        "species": [],
        "starships": ["https://swapi.dev/api/starships/12/"],
        "vehicles": ["https://swapi.dev/api/vehicles/14/"]
    }

    with aioresponses() as m:
        m.get("https://swapi.dev/api/planets/1/", payload={"name": "Tatooine"})
        m.get("https://swapi.dev/api/films/1/", payload={"title": "A New Hope"})
        m.get("https://swapi.dev/api/starships/12/", payload={"name": "X-wing"})
        m.get("https://swapi.dev/api/vehicles/14/", payload={"name": "Snowspeeder"})

        character = await process_character(item, session)
        
        assert character['name'] == "Luke Skywalker"
        assert character['homeworld'] == "Tatooine"
        assert character['films'] == ["A New Hope"]
        assert character['starships'] == ["X-wing"]
        assert character['vehicles'] == ["Snowspeeder"]