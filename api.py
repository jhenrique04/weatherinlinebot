import os
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_weather(session, city: str):
    async with session.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.environ.get('OW_API_KEY')}&units=metric") as response:
        return await response.json()


async def get_forecast(session, city: str):
    async with session.get(f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={os.environ.get('OW_API_KEY')}&units=metric") as response:
        return await response.json()


async def get_coordinates(session, city: str):
    async with session.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={os.environ.get('OW_API_KEY')}") as response:
        data = await response.json()
        if data and isinstance(data, list) and len(data) > 0:
            return data[0]['lat'], data[0]['lon']
        else:
            return None, None


async def get_air_pollution(session, lat: str, lon: str):
    async with session.get(f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={os.environ.get('OW_API_KEY')}") as response:
        return await response.json()


async def get_weather_map(session, layer: str, lat: str, lon: str, zoom=1):
    async with session.get(f"https://tile.openweathermap.org/map/{layer}/{zoom}/{lat}/{lon}.png?appid={os.environ.get('OW_API_KEY')}") as response:
        if response.status == 200:
            return response.url
        else:
            logger.error(f"Failed to get weather map: {response.status}, {response.text}")
            return None