import pytest
import asyncpg
from db import create_table, insert_characters
from models import Character

@pytest.mark.asyncio
async def test_create_table():
    conn = await asyncpg.connect(user='postgres', password='postgres', database='postgres', host='localhost')
    await create_table()
    result = await conn.fetch("SELECT * FROM information_schema.tables WHERE table_name='characters'")
    assert len(result) == 1
    await conn.close()

@pytest.mark.asyncio
async def test_insert_characters():
    conn = await asyncpg.connect(user='postgres', password='postgres', database='postgres', host='localhost')
    await create_table()

    character = Character(
        id=1,
        birth_year="19BBY",
        eye_color="Blue",
        films=["A New Hope"],
        gender="Male",
        hair_color="Blond",
        height="172",
        homeworld="Tatooine",
        mass="77",
        name="Luke Skywalker",
        skin_color="Fair",
        species=["Human"],
        starships=["X-wing"],
        vehicles=["Snowspeeder"]
    )

    await insert_characters([character.model_dump()])

    result = await conn.fetch("SELECT * FROM characters WHERE id=1")
    assert len(result) == 1
    assert result[0]['name'] == "Luke Skywalker"

    await conn.close()
