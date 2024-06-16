import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from db.config import Base, init_db

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
async def test_init_db(engine):
    assert engine