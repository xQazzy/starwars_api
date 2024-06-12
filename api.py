import aiohttp

async def fetch_character(session, character_id):
    character_url = f'https://swapi.dev/api/people/{character_id}/'
    async with session.get(character_url) as response:
        if response.status == 200:
            return await response.json()
        else:
            return None

async def fetch_characters(start_id, end_id):
    characters = []
    async with aiohttp.ClientSession() as session:
        for character_id in range(start_id, end_id + 1):
            character_data = await fetch_character(session, character_id)
            if character_data is not None:
                characters.append(character_data)
    return characters
