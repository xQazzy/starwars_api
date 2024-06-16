import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from db.config import Base
from db.models import Character

@pytest.fixture(scope='function')
async def engine():
    async_engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/temp_db", echo=True)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_engine
    await async_engine.dispose()

@pytest.fixture(scope='function')
async def session(engine):
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session

@pytest.mark.asyncio
async def test_create_and_unique_character(session):
    character = Character(
        name='Luke Skywalker',
        birth_year='19BBY',
        eye_color='blue',
        gender='male',
        hair_color='blond',
        height='172',
        mass='77',
        skin_color='fair',
        homeworld='Tatooine',
        films=['A New Hope'],
        species=['Human'],
        starships=['X-wing'],
        vehicles=['Speeder Bike']
    )
    session.add(character)
    await session.commit()
    result = await session.execute(select(Character).filter_by(name='Luke Skywalker'))
    character_from_db = result.scalars().first()
    assert character_from_db is not None
    assert character_from_db.name == 'Luke Skywalker'