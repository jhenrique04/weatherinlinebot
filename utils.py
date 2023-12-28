import datetime
import math
from uuid import uuid4
from telegram import InlineQueryResultArticle, InputTextMessageContent

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


def celsius_to_fahrenheit(celsius):
    return f"{celsius * 9 / 5 + 32 :.2f}"


def lat_lon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x_tile = int((lon + 180.0) / 360.0 * n)
    y_tile = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return x_tile, y_tile


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
                f"{forecast_date.date()}: {temp}°C / {celsius_to_fahrenheit(temp)}°F, {description} {emoji}")
    return "\n".join(message_lines)