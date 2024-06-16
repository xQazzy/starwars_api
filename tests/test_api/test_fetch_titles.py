import pytest
from aioresponses import aioresponses
from api.fetch_titles import fetch_homeworld_name, fetch_film_names, fetch_species_names, fetch_starship_names, fetch_vehicle_names
import aiohttp

@pytest.fixture
async def session():
    async with aiohttp.ClientSession() as session:
        yield session

@pytest.mark.asyncio
async def test_fetch_homeworld_name(session):
    url = 'https://swapi.dev/api/planets/1/'
    with aioresponses() as m:
        m.get(url, payload={'name': 'Tatooine'})
        
        name = await fetch_homeworld_name(url, session)
        assert name == 'Tatooine'

@pytest.mark.asyncio
async def test_fetch_film_names(session):
    urls = [
        'https://swapi.dev/api/films/1/',
        'https://swapi.dev/api/films/2/'
    ]
    with aioresponses() as m:
        m.get(urls[0], payload={'title': 'A New Hope'})
        m.get(urls[1], payload={'title': 'The Empire Strikes Back'})
        
        names = await fetch_film_names(urls, session)
        assert names == ['A New Hope', 'The Empire Strikes Back']

@pytest.mark.asyncio
async def test_fetch_species_names(session):
    urls = [
        'https://swapi.dev/api/species/1/',
        'https://swapi.dev/api/species/2/'
    ]
    with aioresponses() as m:
        m.get(urls[0], payload={'name': 'Human'})
        m.get(urls[1], payload={'name': 'Droid'})
        
        names = await fetch_species_names(urls, session)
        assert names == ['Human', 'Droid']

@pytest.mark.asyncio
async def test_fetch_starship_names(session):
    urls = [
        'https://swapi.dev/api/starships/1/',
        'https://swapi.dev/api/starships/2/'
    ]
    with aioresponses() as m:
        m.get(urls[0], payload={'name': 'X-wing'})
        m.get(urls[1], payload={'name': 'TIE Fighter'})
        
        names = await fetch_starship_names(urls, session)
        assert names == ['X-wing', 'TIE Fighter']

@pytest.mark.asyncio
async def test_fetch_vehicle_names(session):
    urls = [
        'https://swapi.dev/api/vehicles/1/',
        'https://swapi.dev/api/vehicles/2/'
    ]
    with aioresponses() as m:
        m.get(urls[0], payload={'name': 'Snowspeeder'})
        m.get(urls[1], payload={'name': 'Speeder bike'})
        
        names = await fetch_vehicle_names(urls, session)
        assert names == ['Snowspeeder', 'Speeder bike']
