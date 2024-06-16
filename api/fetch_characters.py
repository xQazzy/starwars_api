import asyncio
import logging
from aiohttp import ClientSession
from .fetch_titles import fetch_film_names, fetch_species_names, fetch_starship_names, fetch_vehicle_names, fetch_homeworld_name

async def fetch_characters(session: ClientSession):
    url = "https://swapi.dev/api/people/"
    characters = []

    while url:
        async with session.get(url) as response:
            data = await response.json()
            tasks = []

            for item in data['results']:
                tasks.append(process_character(item, session))
                
            characters_batch = await asyncio.gather(*tasks, return_exceptions=True)
            characters.extend([char for char in characters_batch if isinstance(char, dict)])

            url = data.get('next')

    return characters

async def process_character(item: dict, session: ClientSession):
    try:
        return {
            'name': item['name'],
            'height': item['height'],
            'mass': item['mass'],
            'hair_color': item['hair_color'],
            'skin_color': item['skin_color'],
            'eye_color': item['eye_color'],
            'birth_year': item['birth_year'],
            'gender': item['gender'],
            'homeworld': await fetch_homeworld_name(item['homeworld'], session),
            'films': await fetch_film_names(item['films'], session),
            'species': await fetch_species_names(item['species'], session),
            'starships': await fetch_starship_names(item['starships'], session),
            'vehicles': await fetch_vehicle_names(item['vehicles'], session)
        }
    except Exception as e:
        logging.error(f"Ошибка обработки персонажа {item['name']}: {e}")
        return None