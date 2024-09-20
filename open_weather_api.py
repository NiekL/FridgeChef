import os
import requests
from dotenv import load_dotenv

load_dotenv()

# OpenWeather API credentials and Base URL
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_URL = os.getenv("OPENWEATHER_BASE_URL")


def get_weather(city_name):
    """ Fetch the current weather for a city using OpenWeather API. """
    params = {
        'q': city_name,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(OPENWEATHER_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        # Exception handling, logs the message
        print(f"Probleem met ophalen weerdata: {e}")
        return None

def select_recipe_type_by_weather(temp, weather_condition):
    """ Select a recipe type based on temperature and weather condition. """
    if weather_condition in ['snow', 'rain']:
        if temp < 5:
            return 'hot chocolate'
        elif temp < 10:
            return 'soup'
        else:
            return 'stew'
    else:  # Clear or clouded weather
        if temp < 10:
            return 'baked pasta'
        elif temp < 15:
            return 'roast'
        elif temp < 20:
            return 'grilled sandwich'
        elif temp < 25:
            return 'salad'
        elif temp < 30:
            return 'smoothie'
        else:
            return 'ice cream'