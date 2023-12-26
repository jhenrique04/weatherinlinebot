import os
import logging
import requests
import sys
import datetime
import math
from uuid import uuid4
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

conditions = {
    "Thunderstorm": "⛈️",  # Thunderstorms
    "Drizzle": "🌧️",  # Drizzle
    "Rain": "🌦️",  # Rain
    "Snow": "❄️",  # Snow
    "Mist": "🌫️",  # Mist
    "Smoke": "💨",  # Smoke
    "Haze": "🌁",  # Haze
    "Dust": "🌪️",  # Dust whirls
    "Fog": "🌫️",  # Fog
    "Sand": "🏜️",  # Sand
    "Ash": "🌋",  # Volcanic ash
    "Squall": "🌬️",  # Squalls
    "Tornado": "🌪️",  # Tornado
    "Clear": "☀️",  # Clear sky
    "Clouds": "☁️"  # Clouds
}


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to the Weather Bot! Type the name of a city to get weather updates.")


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Type the name of a city in inline mode to get weather information.\nFor example:\n@YourBotName New York\nOr, if you want a 5-day forecast:\n@YourBotName forecast New York")


def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.environ.get('OW_API_KEY')}&units=metric"
    response = requests.get(url)
    return response.json()


def get_forecast(city: str):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={os.environ.get('OW_API_KEY')}&units=metric"
    response = requests.get(url)
    return response.json()


def get_coordinates(city: str):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={os.environ.get('OW_API_KEY')}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        return None, None


def get_air_pollution(lat: str, lon: str):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={os.environ.get('OW_API_KEY')}"
    response = requests.get(url)
    return response.json()


def lat_lon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x_tile = int((lon + 180.0) / 360.0 * n)
    y_tile = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return x_tile, y_tile


def get_weather_map(layer: str, lat: str, lon: str, zoom=1):
    url = f"https://tile.openweathermap.org/map/{layer}/{zoom}/{lat}/{lon}.png?appid={os.environ.get('OW_API_KEY')}"
    response = requests.get(url)
    if response.status_code == 200:
        print(url)
        return url
    else:
        logger.error(f"Failed to get weather map: {response.status_code}, {response.text}")
        return None


def create_article(title, message):
    return InlineQueryResultArticle(
        id=uuid4(),
        title=title,
        description=message,
        input_message_content=InputTextMessageContent(
            message_text=f"{title}\n{message}",
            parse_mode="Markdown"
        )
    )


def format_forecast_message(forecast_data):
    message_lines = []
    for day_data in forecast_data['list']:
        forecast_date = datetime.datetime.fromtimestamp(day_data['dt'])
        if forecast_date.hour == 12:
            condition = day_data['weather'][0]['main']
            emoji = conditions.get(condition, "")
            temp = day_data['main']['temp']
            description = day_data['weather'][0]['description'].title()
            message_lines.append(
                f"{forecast_date.date()}: {temp}°C, {description} {emoji}")
    return "\n".join(message_lines)


def inlinequery(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    results = []

    if not query.strip():
        results.append(InlineQueryResultArticle(
            id=uuid4(),
            title="Type a city name to get weather information.",
            input_message_content=InputTextMessageContent(
                message_text="Please type a city name to get weather information."
            )
        ))
        update.inline_query.answer(results, cache_time=10)
        return

    if query.lower().startswith("forecast "):
        city = query.split(" ", 1)[1].strip()
        forecast_data = get_forecast(city)
        if forecast_data and 'list' in forecast_data:
            message = format_forecast_message(forecast_data)
            results.append(create_article(
                f"5-Day Forecast for {city.title()}", message))
        else:
            results.append(create_article("Forecast not found",
                           "Could not retrieve the forecast."))

    if query.lower().startswith("map clouds "):
        city = query.split(" ", 2)[2].strip()
        lat, lon = get_coordinates(city)
        if lat and lon:
            x_tile, y_tile = lat_lon_to_tile(lat, lon, 1)
            map_url = get_weather_map("clouds_new", x_tile, y_tile)
            results.append(InlineQueryResultArticle(
                id=uuid4(),
                title=f"Clouds Map for {city.title()}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Clouds Map for {city.title()}: [View Map]({map_url})",
                    parse_mode="Markdown"
                ),
                thumb_url=map_url,
                description="Clouds Map"
            ))
        else:
            results.append(create_article("Map not found",
                           "Could not retrieve the map."))
            
    if query.lower().startswith("map precipitation "):
        city = query.split(" ", 2)[2].strip()
        lat, lon = get_coordinates(city)
        if lat and lon:
            x_tile, y_tile = lat_lon_to_tile(lat, lon, 1)
            map_url = get_weather_map("precipitation_new", x_tile, y_tile)
            results.append(InlineQueryResultArticle(
                id=uuid4(),
                title=f"Precipitation Map for {city.title()}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Precipitation Map for {city.title()}: [View Map]({map_url})",
                    parse_mode="Markdown"
                ),
                thumb_url=map_url,
                description="Precipitation Map"
            ))
        else:
            results.append(create_article("Map not found",
                           "Could not retrieve the map."))
            
    if query.lower().startswith("map pressure "):
        city = query.split(" ", 2)[2].strip()
        lat, lon = get_coordinates(city)
        if lat and lon:
            x_tile, y_tile = lat_lon_to_tile(lat, lon, 1)
            map_url = get_weather_map("pressure_new", x_tile, y_tile)
            results.append(InlineQueryResultArticle(
                id=uuid4(),
                title=f"Pressure Map for {city.title()}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Pressure Map for {city.title()}: [View Map]({map_url})",
                    parse_mode="Markdown"
                ),
                thumb_url=map_url,
                description="Pressure Map"
            ))
        else:
            results.append(create_article("Map not found",
                           "Could not retrieve the map."))
            
    if query.lower().startswith("map wind "):
        city = query.split(" ", 2)[2].strip()
        lat, lon = get_coordinates(city)
        if lat and lon:
            x_tile, y_tile = lat_lon_to_tile(lat, lon, 1)
            map_url = get_weather_map("wind_new", x_tile, y_tile)
            results.append(InlineQueryResultArticle(
                id=uuid4(),
                title=f"Wind Map for {city.title()}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Wind Map for {city.title()}: [View Map]({map_url})",
                    parse_mode="Markdown"
                ),
                thumb_url=map_url,
                description="Wind Map"
            ))
        else:
            results.append(create_article("Map not found",
                           "Could not retrieve the map."))
            
    if query.lower().startswith("map temperature "):
        city = query.split(" ", 2)[2].strip()
        lat, lon = get_coordinates(city)
        if lat and lon:
            x_tile, y_tile = lat_lon_to_tile(lat, lon, 1)
            map_url = get_weather_map("temp_new", x_tile, y_tile)
            results.append(InlineQueryResultArticle(
                id=uuid4(),
                title=f"Temperature Map for {city.title()}",
                input_message_content=InputTextMessageContent(
                    message_text=f"Temperature Map for {city.title()}: [View Map]({map_url})",
                    parse_mode="Markdown"
                ),
                thumb_url=map_url,
                description="Temperature Map"
            ))
        else:
            results.append(create_article("Map not found",
                           "Could not retrieve the map."))
    
    else:
        weather_data = get_weather(query)
        lat, lon = get_coordinates(query)
        air_pollution = get_air_pollution(lat, lon)
        if weather_data and 'weather' in weather_data:
            condition = weather_data['weather'][0]['main']
            emoji = conditions.get(condition, "")
            title = f"Current Weather in {query.title()}"
            description = f"Temp: {weather_data['main']['temp']}°C, {weather_data['weather'][0]['description'].title()} {emoji}\nAir Pollution Index (1-5): {air_pollution['list'][0]['main']['aqi']}"
            results.append(create_article(title, description))

    update.inline_query.answer(results, cache_time=10)


def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f"Update {update} caused error {context.error}")


def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        logger.critical(
            "No BOT_TOKEN environment variable found. Terminating.")
        sys.exit(1)

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()