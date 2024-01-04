# Weather Bot for Telegram

## Description

This Telegram bot allows users to search for weather information using the OpenWeatherMap API. Users can get current weather data, a 5-day forecast, meteorological conditions for a specified location and various types of maps (clouds, precipitation, pressure, wind and temperature) directly within Telegram.

## Features

- Search for current weather data by city name.

- Get information of the current date and time of the city.

- Get the current weather information (temperature, pressure, wind speed, humidity, cloud cover...)

- Get a 5-day weather forecast.

- Access various weather maps including clouds, precipitation, pressure, wind, and temperature maps.

- Inline query support for quick weather updates.

## Requirements

- Python 3
- Telegram Bot Token
- OpenWeather API Key
- Libraries: aiohttp, python-telegram-bot

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

In Telegram, use the bot's username and the name of the city that you want to know the current weather information or type map followed by a weather type map and the city name. For example:

    @YourBotUsername Fortaleza
    @YourBotUsername map clouds Worldwide
    @YourBotUsername map precipitation Worldwide
    @YourBotUsername map pressure Worldwide
    @YourBotUsername map wind Worldwide
    @YourBotUsername map temperature Worldwide


The outputs, respectively, should look something like this:

    Weather in Fortaleza-BR -3.72 / -38.52
    As Of: 2024-01-04 06:37:08
    Right Now: Scattered Clouds ☁️
    Temp: 28.32°C / 82.98°F
    Pressure: 1012 hPa
    Wind Speed: 2.57 m/s
    Humidity: 84%
    Cloud Cover: 40%

    Forecast Summary:
    2024-01-04: 29.53°C / 85.15°F, Few Clouds ☁️
    2024-01-05: 30.13°C / 86.23°F, Scattered Clouds ☁️
    2024-01-06: 30.22°C / 86.40°F, Light Rain 🌦️
    2024-01-07: 30.06°C / 86.11°F, Scattered Clouds ☁️
    2024-01-08: 30.35°C / 86.63°F, Light Rain 🌦️

Clouds Map for Worldwide: View Map

![Clouds map](https://raw.githubusercontent.com/jhenrique04/weatherinlinebot/master/images/clouds.jpg)

Precipitation Map for Worldwide: View Map

![Precipitation map](https://raw.githubusercontent.com/jhenrique04/weatherinlinebot/master/images/precipitation.jpg)

Pressure Map for Worldwide: View Map

![Pressure map](https://raw.githubusercontent.com/jhenrique04/weatherinlinebot/master/images/pressure.jpg)

Wind Map for Worldwide: View Map

![Wind map](https://raw.githubusercontent.com/jhenrique04/weatherinlinebot/master/images/wind.jpg)

Temperature Map for Worldwide: View Map

![Temperature map](https://raw.githubusercontent.com/jhenrique04/weatherinlinebot/master/images/temperature.jpg)

## Contributing

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

Contributions, issues, and feature requests are welcome. Feel free to check issues page if you want to contribute.

Original Author: @zeapenas - jhenriquevs.04@gmail.com