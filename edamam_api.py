import os
import random

import requests
from dotenv import load_dotenv

load_dotenv()

# Edamam API credentials and Base URL
APP_ID = os.getenv("EDAMAM_APP_ID")
APP_KEY = os.getenv("EDAMAM_API_KEY")
BASE_URL = os.getenv("EDAMAM_BASE_URL")


def get_random_recipe(query):
    """Fetch a random recipe using Edamam API v2"""

    # List of possible search queries to vary the results because there is no random option in the API without using a query
    random_query = random.choice(query)

    # Recipe query parameters (adapted for Edamam v2)
    params = {
        'type': 'public',  # Required in v2, specify recipe type
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'q': random_query,
        'random': True,  # Enable random recipe fetching
        'to': 1  # Fetch only one random recipe
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Will raise HTTPError for bad responses
        data = response.json()
        recipe = data['hits'][0]['recipe'] if data.get('hits') else None
        if recipe:
            return recipe
        else:
            print("Geen recepten gevonden.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Er is iets mis gegaan tijdens het ophalen van de recepten: {e}")
        return None


def get_recipe_based_on_fridge(ingredients):
    """Fetch a recipe using a more selective approach from the Edamam API."""

    # Choose up to 3 key ingredients randomly from the list to form a query
    key_ingredients = random.sample(ingredients, min(len(ingredients), 3))

    params = {
        'type': 'public',
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'q': ','.join(key_ingredients),  # Using key ingredients for the query
        'random': True,
        'to': 1
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Will raise HTTPError for bad responses
        data = response.json()
        recipe = data['hits'][0]['recipe'] if data.get('hits') else None
        if recipe:
            return recipe
        else:
            print("Geen recepten gevonden.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Er is iets mis gegaan tijdens het ophalen van de recepten: {e}")
        return None
