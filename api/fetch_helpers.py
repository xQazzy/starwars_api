import aiohttp
import logging

async def fetch_title(url, session):
    try:
        async with session.get(url) as response:
            if response.status != 200:
                logging.error(f"Ошибка получения данных {url}: {response.status}")
                return None
            data = await response.json()
            return data.get('title') or data.get('name')
    except aiohttp.ContentTypeError as e:
        logging.error(f"Ошибка типа контента {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"Ошибка получения заголовка из {url}: {e}")
        return None