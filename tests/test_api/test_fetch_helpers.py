import pytest
import aiohttp
from aioresponses import aioresponses
from api.fetch_helpers import fetch_title

@pytest.fixture
async def session():
    async with aiohttp.ClientSession() as session:
        yield session

@pytest.mark.asyncio
async def test_fetch_title_success(session):
    url = 'https://swapi.dev/api/films/1/'
    with aioresponses() as m:
        m.get(url, payload={'title': 'A New Hope'})
        
        title = await fetch_title(url, session)
        assert title == 'A New Hope'

@pytest.mark.asyncio
async def test_fetch_title_name_fallback(session):
    url = 'https://swapi.dev/api/people/1/'
    with aioresponses() as m:
        m.get(url, payload={'name': 'Luke Skywalker'})
        
        title = await fetch_title(url, session)
        assert title == 'Luke Skywalker'

@pytest.mark.asyncio
async def test_fetch_title_error_status(session):
    url = 'https://swapi.dev/api/invalid/'
    with aioresponses() as m:
        m.get(url, status=404)
        
        title = await fetch_title(url, session)
        assert title is None

@pytest.mark.asyncio
async def test_fetch_title_content_type_error(session):
    url = 'https://swapi.dev/api/films/1/'
    with aioresponses() as m:
        m.get(url, body="Not a JSON", status=200)
        
        title = await fetch_title(url, session)
        assert title is None

@pytest.mark.asyncio
async def test_fetch_title_exception(session):
    url = 'https://swapi.dev/api/films/1/'
    with aioresponses() as m:
        m.get(url, exception=aiohttp.ClientError)
        
        title = await fetch_title(url, session)
        assert title is None