import asyncio
import logging
from aiohttp import ClientSession
from db.config import init_db, SessionLocal
from db.crud import add_character
from api.fetch_characters import fetch_characters
import time

logging.basicConfig(level=logging.INFO)

async def main():
    logging.info("Начало инициализации базы данных...")
    await init_db()
    logging.info("Инициализация базы данных завершена.")

    async with ClientSession() as session:
        logging.info("Получаем персонажей...")
        start_time = time.time()
        characters = await fetch_characters(session)
        logging.info(f"Получено {len(characters)} персонажей. Время загрузки: {time.time() - start_time:.2f} секунд.")

    async def add_character_task(character):
        async with SessionLocal() as db_session:
            task_start_time = time.time()
            logging.info(f"Начало добавления персонажа {character['name']} в {task_start_time:.2f} секунд.")
            await add_character(db_session, character)
            logging.info(f"Завершено добавление персонажа {character['name']} в {time.time() - task_start_time:.2f} секунд.")

    tasks = [add_character_task(character) for character in characters]
    await asyncio.gather(*tasks)
    logging.info(f"Все задачи завершены за {time.time() - start_time:.2f} секунд.")

if __name__ == '__main__':
    asyncio.run(main())