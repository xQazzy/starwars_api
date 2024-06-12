import asyncpg
from models import Character
import logging

logger = logging.getLogger(__name__)

async def create_table():
    conn = await asyncpg.connect(user='postgres', password='postgres', database='postgres', host='localhost')

    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS characters (
            id SERIAL PRIMARY KEY,
            birth_year TEXT,
            eye_color TEXT,
            films TEXT,
            gender TEXT,
            hair_color TEXT,
            height TEXT,
            homeworld TEXT,
            mass TEXT,
            name TEXT,
            skin_color TEXT,
            species TEXT,
            starships TEXT,
            vehicles TEXT
        )
        """
    )

    await conn.close()

async def insert_characters(characters):
    conn = await asyncpg.connect(user='postgres', password='postgres', database='postgres', host='localhost')

    await conn.execute("TRUNCATE TABLE characters RESTART IDENTITY")

    formatted_data = []
    for character_id, character_data in enumerate(characters, start=1):
        try:
            character_data['id'] = character_id
            character_model = Character(**character_data)
            formatted_data.append((
                character_model.id,
                character_model.birth_year,
                character_model.eye_color,
                ', '.join(character_model.films),
                character_model.gender,
                character_model.hair_color,
                character_model.height,
                character_model.homeworld,
                character_model.mass,
                character_model.name,
                character_model.skin_color,
                ', '.join(character_model.species),
                ', '.join(character_model.starships),
                ', '.join(character_model.vehicles)
            ))
        except Exception as e:
            logger.error(f"Error processing character with id {character_id}: {e}")

    await conn.executemany(
        """
        INSERT INTO characters (id, birth_year, eye_color, films, gender, hair_color, height, homeworld, mass, name, skin_color, species, starships, vehicles)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
        """,
        formatted_data
    )

    await conn.close()
