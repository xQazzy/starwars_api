import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from .models import Character

async def add_character(session: AsyncSession, character_data: dict):
    try:
        query = select(Character).filter_by(name=character_data['name'])
        result = await session.execute(query)
        existing_character = result.scalars().first()

        if existing_character:
            logging.info(f"Персонаж {character_data['name']} уже существует в базе данных.")
            return

        character = Character(**character_data)
        session.add(character)
        await session.commit()
    except IntegrityError as e:
        logging.error(f"Ошибка добавления персонажа {character_data['name']}: {e}")
        await session.rollback()
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")
        await session.rollback()