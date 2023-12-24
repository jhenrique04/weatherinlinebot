# Weather Bot for Telegram

## Description

This Telegram bot allows users to search for weather information using the OpenWeatherMap API. Users can get current weather data, a 5-day forecast, and meteorological conditions for a specified location directly within Telegram.

## Features

- Search for current weather data by city name.

- Get a 5-day weather forecast.

- Get the Air Pullution Index (AQI).

- Inline query support for quick weather updates.

## Requirements

- Python 3
- Telegram Bot Token
- OpenWeather API Key
- Libraries: requests, python-telegram-bot

## Setup

Install the required Python packages with:

    pip install -r requirements.txt


You can set the Telegram Bot Token and the OpenWeather API Key using export:

    export BOT_TOKEN=your_telegram_bot_token
    export OW_API_KEY=your_openweather_api_key

But you can also create a .env file with the token/key inside of it.

- Remember that the bot needs to be setted to inline.


## Usage

Run the bot locally with the following command:

    python main.py

Or, if you created the .env file:
    
    set -a; source .env; set +a; python main.py   

In Telegram, use the bot's username and the name of the city that you want to know the current weather or type forecast followed by the name of the city to get a 5 day weather forecast. For example:

    @YourBotUsername Fortaleza
    @YourBotUsername forecast Fortaleza

The outputs, respectively, should look something like this:

    Current Weather in Fortaleza
    Temp: 27.07°C, Scattered Clouds ☁️
    Air Pollution Index (1-5): 1
        
    5-Day Forecast for Fortaleza
    2023-12-24: 30.14°C, Scattered Clouds ☁️
    2023-12-25: 29.93°C, Scattered Clouds ☁️
    2023-12-26: 29.24°C, Light Rain 🌦️
    2023-12-27: 29.57°C, Light Rain 🌦️
    2023-12-28: 29.79°C, Broken Clouds ☁️

## Contributing

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

Contributions, issues, and feature requests are welcome. Feel free to check issues page if you want to contribute.

Original Author: @zeapenas - jhenriquevs.04@gmail.com