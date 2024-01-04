import aiohttp
import datetime
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext
from uuid import uuid4
from api import get_weather, get_forecast, get_coordinates, get_weather_map
from utils import conditions, celsius_to_fahrenheit, lat_lon_to_tile, create_article, format_forecast_message, create_empty_query_result, create_invalid_command_result


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome to the Weather Bot! Type the name of a city to get weather updates.")


async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Type the name of a city in inline mode to get weather information.\nFor example:\n@YourBotName New York\nOr, if you want a 5-day forecast:\n@YourBotName forecast New York")


async def parse_command(query: str) -> tuple:
    parts = query.lower().split(" ", 1)
    command = parts[0]
    args = parts[1].strip() if len(parts) > 1 else ""

    return command, args


async def handle_map_command(session: aiohttp.ClientSession, city: str, map_type: str) -> InlineQueryResultArticle:
    map_types = {"clouds": "clouds_new", "precipitation": "precipitation_new",
                 "pressure": "pressure_new", "wind": "wind_new", "temperature": "temp_new"}

    if map_type in map_types and city:
        layer = map_types[map_type]
        lat, lon = await get_coordinates(session, city)
        if lat and lon:
            x_tile, y_tile = lat_lon_to_tile(lat, lon, 1)
            map_url = await get_weather_map(session, layer, x_tile, y_tile)
            if map_url:
                return InlineQueryResultArticle(
                    id=uuid4(),
                    title=f"{map_type.capitalize()} Map for {city.title()}",
                    input_message_content=InputTextMessageContent(
                        message_text=f"{map_type.capitalize()} Map for {city.title()}: [View Map]({map_url})",
                        parse_mode="Markdown"
                    ),
                    description=f"{map_type.capitalize()} Map"
                )
            else:
                return create_article("Map not found", "Could not retrieve the map.")
        else:
            return create_article("Invalid city", "Could not find coordinates for the specified city.")
    else:
        return create_article("Incomplete command", "Please provide a map type and a city name.")


async def handle_weather_command(session: aiohttp.ClientSession, city: str) -> InlineQueryResultArticle:
    weather_data = await get_weather(session, city)
    forecast_data = await get_forecast(session, city)
    if weather_data.get('weather'):
        condition = weather_data['weather'][0]['main']
        emoji = conditions.get(condition, "")
        temp = weather_data['main']['temp']
        temp_fahrenheit = celsius_to_fahrenheit(temp)
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        wind_speed = weather_data['wind']['speed']
        clouds = weather_data['clouds']['all']
        dt = datetime.datetime.fromtimestamp(weather_data['dt']).strftime('%Y-%m-%d %H:%M:%S')
        city_name = weather_data['name']
        country = weather_data['sys']['country']
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']

        title = f"Weather in {city_name}-{country} {lat:.2f} / {lon:.2f}"
        description = (
            f"As Of: {dt}\n"
            f"Right Now: {weather_data['weather'][0]['description'].title()} {emoji}\n"
            f"Temp: {temp}°C / {temp_fahrenheit}°F\n"
            f"Pressure: {pressure} hPa\n"
            f"Wind Speed: {wind_speed} m/s\n"
            f"Humidity: {humidity}%\n"
            f"Cloud Cover: {clouds}%\n"
        )

        if forecast_data and 'list' in forecast_data:
             forecast_summary = format_forecast_message(forecast_data)
             description += f"\nForecast Summary:\n{forecast_summary}"

        return create_article(title, description)
    else:
        return create_article("Data not found", "Could not retrieve weather data. Please try again later or check the city name.")


async def inline_query(update, context):
    query = update.inline_query.query
    results = []

    async with aiohttp.ClientSession() as session:
        command, args = await parse_command(query)

        if command == "" or command not in ["map", "forecast"]:
            if args:
                result = await handle_weather_command(session, query)
                results.append(result)
            else:
                results.append(create_empty_query_result())

        elif command == "map":
            map_type, *city_parts = args.split(" ", 1)
            city = " ".join(city_parts).strip() if city_parts else None
            if city:
                result = await handle_map_command(session, city, map_type)
                results.append(result)
            else:
                results.append(create_article("No city provided", "Please provide a city name after the map type."))

        else:
            results.append(create_invalid_command_result())

        await update.inline_query.answer(results, cache_time=10)