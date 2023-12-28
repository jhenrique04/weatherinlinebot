from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext
import aiohttp
from uuid import uuid4
from apis import get_weather, get_forecast, get_coordinates, get_weather_map
from utils import conditions, celsius_to_fahrenheit, lat_lon_to_tile, create_article, format_forecast_message


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome to the Weather Bot! Type the name of a city to get weather updates.")


async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Type the name of a city in inline mode to get weather information.\nFor example:\n@YourBotName New York\nOr, if you want a 5-day forecast:\n@YourBotName forecast New York")


async def inlinequery(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    results = []

    async with aiohttp.ClientSession() as session:
        command, *args = query.lower().split(" ", 1)
        args = args[0].strip() if args else None

        match command:
            case "forecast":
                if args:
                    city = args
                    forecast_data = await get_forecast(session, city)
                    if forecast_data and 'list' in forecast_data:
                        message = format_forecast_message(forecast_data)
                        results.append(create_article(f"5-Day Forecast for {city.title()}", message))
                    else:
                        results.append(create_article("Forecast not found", "Could not retrieve the forecast."))
                else:
                    results.append(create_article("No city provided", "Please provide a city name for the forecast."))
                await update.inline_query.answer(results, cache_time=10)

            case "map":
                if args:
                    map_type, *city_parts = args.split(" ")
                    city = " ".join(city_parts).strip()
                    map_types = {"clouds": "clouds_new", "precipitation": "precipitation_new",
                                 "pressure": "pressure_new", "wind": "wind_new", "temperature": "temp_new"}

                    if map_type in map_types and city:
                        layer = map_types[map_type]
                        lat, lon = await get_coordinates(session, city)
                        if lat and lon:
                            x_tile, y_tile = lat_lon_to_tile(lat, lon, 1)
                            map_url = await get_weather_map(session, layer, x_tile, y_tile)
                            if map_url:
                                results.append(InlineQueryResultArticle(
                                    id=uuid4(),
                                    title=f"{map_type.capitalize()} Map for {city.title()}",
                                    input_message_content=InputTextMessageContent(
                                        message_text=f"{map_type.capitalize()} Map for {city.title()}: [View Map]({map_url})",
                                        parse_mode="Markdown"
                                    ),
                                    description=f"{map_type.capitalize()} Map"
                                ))
                            else:
                                results.append(create_article("Map not found", "Could not retrieve the map."))
                        else:
                            results.append(create_article("Invalid city", "Could not find coordinates for the specified city."))
                    else:
                        results.append(create_article("Incomplete command", "Please provide a map type and a city name."))
                else:
                    results.append(create_article("No city provided", "Please provide a city name after the map type."))
                await update.inline_query.answer(results, cache_time=10)

            case _:
                weather_data = await get_weather(session, query)
                if weather_data and 'weather' in weather_data:
                    condition = weather_data['weather'][0]['main']
                    emoji = conditions.get(condition, "")
                    title = f"Current Weather in {query.title()}"
                    description = f"Temp: {weather_data['main']['temp']}°C / {celsius_to_fahrenheit(weather_data['main']['temp'])}°F.\nRight Now: {weather_data['weather'][0]['description'].title()} {emoji}"
                    results.append(create_article(title, description))
                else:
                    results.append(create_article("City not found", "Could not retrieve weather for the specified city."))
                await update.inline_query.answer(results, cache_time=10)