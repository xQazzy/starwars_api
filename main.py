import asyncio
import aiohttp
import logging
from db import create_table, insert_characters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_character(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_all_characters():
    characters = []
    async with aiohttp.ClientSession() as session:
        page = 1
        while True:
            url = f'https://swapi.dev/api/people/?page={page}'
            response_data = await fetch_character(session, url)
            if 'results' not in response_data:
                break
            characters.extend(response_data['results'])
            logger.info(f"Получено {len(response_data['results'])} персонажей со станицы {page}")
            if response_data['next'] is None:
                break
            page += 1
    logger.info(f"Итогоговое количество персонажей: {len(characters)}")
    return characters

async def main():
    await create_table()
    characters = await fetch_all_characters()
    await insert_characters(characters)

if __name__ == "__main__":
    asyncio.run(main())
