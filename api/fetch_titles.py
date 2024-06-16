from .fetch_helpers import fetch_title
import asyncio

async def fetch_homeworld_name(url, session):
    return await fetch_title(url, session)

async def fetch_film_names(urls, session):
    return await asyncio.gather(*(fetch_title(url, session) for url in urls))

async def fetch_species_names(urls, session):
    return await asyncio.gather(*(fetch_title(url, session) for url in urls))

async def fetch_starship_names(urls, session):
    return await asyncio.gather(*(fetch_title(url, session) for url in urls))

async def fetch_vehicle_names(urls, session):
    return await asyncio.gather(*(fetch_title(url, session) for url in urls))