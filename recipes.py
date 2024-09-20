import os
from dotenv import load_dotenv
from edamam_api import get_random_recipe, get_recipe_based_on_fridge
from open_weather_api import get_weather, select_recipe_type_by_weather
from helper_functions import colored_text, colored_input
from shopping_list import add_recipe_ingredients_to_shopping_list

from fridge import get_fridge_contents

load_dotenv()

# Define recipes folder
RECIPE_FOLDER = os.getenv("RECIPES_FOLDER")

#------------------------------------------
# Folder/file functions
#------------------------------------------


def get_next_file_number():
    """Get the current file number by checking existing files"""
    #Get a list of the files in the recipe folder
    files = os.listdir(RECIPE_FOLDER)

    # Initialize an empty list to store the numbers
    numbers = []
    # Loop through each file in the list of files
    for file in files:
        # Check if the file ends with '.txt' and the part before ' - ' is a digit
        if file.endswith('.txt'):
            # Split the file name at ' - ' and get the first part
            file_prefix = file.split(' - ')[0]

            # Check if the first part is a digit
            if file_prefix.isdigit():
                # Convert the first part to an integer and add it to the list of numbers
                numbers.append(int(file_prefix))

    return max(numbers, default=0) + 1

def save_recipe_to_file(recipe, file_number):
    """Save recipe and its instructions to a text file"""
    recipe_name = recipe['label']
    file_name = f"{file_number} - {recipe_name}.txt"
    file_path = os.path.join(RECIPE_FOLDER, file_name)

    # Recipe details
    meal_type = recipe.get('mealType', ['Onbekend'])
    dish_type = recipe.get('dishType', ['Onbekend'])
    cuisine_type = recipe.get('cuisineType', ['Onbekend'])

    # Recipe content
    recipe_content = (
        f"Recept: {recipe['label']}\n"
        f"Bron: {recipe['source']}\n"
        f"Link naar recept: {recipe['url']}\n\n"
        f"Maaltijdtype: {', '.join(meal_type)}\n"
        f"Gerechtstype: {', '.join(dish_type)}\n"
        f"Keukentype: {', '.join(cuisine_type)}\n\n"
        "Ingrediënten:\n" + '\n'.join([f"  - {ing}" for ing in recipe['ingredientLines']]) +
        f"\n\nCalorieën: {recipe['calories']:.2f}\n"
    )

    # Save to file
    with open(file_path, 'w') as file:
        file.write(recipe_content)

    print(f"Opgeslagen als: {file_name}")

def prompt_save_recipe(recipe):
    """Prompt user to save the recipe if they choose to"""
    file_number = get_next_file_number()
    save_recipe_check = colored_input("\nWilt u dit recept opslaan als bestand? (ja/nee) ", "magenta")

    if save_recipe_check.lower() == 'ja':
        save_recipe_to_file(recipe, file_number)

def add_recipe_to_shopping_list(ingredients):
    # Vraag de gebruiker om bevestiging of ze de missende ingrediënten willen toevoegen aan het boodschappenlijstje
    add_to_list = colored_input("\nIngrediënten toevoegen aan boodschappenlijstje? (ja/nee): ",   "magenta").lower()

    if add_to_list == 'ja':
        add_recipe_ingredients_to_shopping_list(ingredients)
    else:
        colored_text("\nIngrediënten zijn niet toegevoegd aan het boodschappenlijstje.", "red")

#------------------------------------------
# Recipes functions
#------------------------------------------

def generate_random_recipe():
    """Get a random recipe from the Edamam API"""
    colored_text("\nWillekeurig recept wordt gegenereerd....\n", "cyan")

    # List of possible search queries to vary the results because there is no random option in the API without using a query
    categories = ['chicken', 'beef', 'vegetarian', 'pasta', 'soup', 'cake', 'salad', 'fish', 'pizza', 'breakfast']
    recipe = get_random_recipe(categories)

    if recipe:
        #Give the recipe details in the terminal
        print_recipe_details(recipe)

        #Ask user to add the ingredients to the shopping list
        ingredients = get_recipe_ingredients(recipe)
        add_recipe_to_shopping_list(ingredients)

        # Ask user to save the recipe
        prompt_save_recipe(recipe)


def make_recipe_from_fridge():
    """Check if a recipe can be made based on fridge contents and optionally add missing ingredients to shopping list."""
    colored_text("\nRecept op basis van koelkast voorraad wordt gegenereerd....\n", "cyan")
    fridge_ingredients = get_fridge_contents()

    recipe = get_recipe_based_on_fridge(fridge_ingredients)
    if recipe:

        recipe_ingredients = get_recipe_ingredients(recipe)

        # Initialize an empty list to store missing ingredients
        missing_ingredients = []
        # Iterate over each item in recipe_ingredients
        for item in recipe_ingredients:
            if item not in fridge_ingredients:
                missing_ingredients.append(item)

        print_recipe_details(recipe)
        if not missing_ingredients:
            colored_text("\nJe hebt alle producten in huis voor dit recept", "green")
        else:
            colored_text("\nLET OP: Je mist nog een aantal ingrediënten voor dit recept.", "yellow")
            print("Missende ingrediënten:", ', '.join(missing_ingredients))

            add_recipe_to_shopping_list(missing_ingredients)

        prompt_save_recipe(recipe)
    else:
        print("Geen recept gevonden op basis van je koelkast inhoud. Zitten er producten in je koelkast?")


def generate_recipe_based_on_weather():
    """Generate recipe suggestions based on current weather in a city."""
    cityname = colored_input("Voer de plaatsnaam in: ", "magenta")

    weather_data = get_weather(cityname)
    if weather_data:
        temp = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
        recipe_type = select_recipe_type_by_weather(temp, weather_description)  # Pass both temp and weather_description
        print(f"Huidige weer in {cityname}: {weather_description}, Temperatuur: {temp}°C")
        print(f"Aanbevolen categorie eten is: {recipe_type}")
        recipe = get_random_recipe(recipe_type)  # Assuming modification in get_random_recipe to accept recipe_type
        if recipe:
            #Print recipe details
            print_recipe_details(recipe)

            # Option to add to shopping list
            ingredients = get_recipe_ingredients(recipe)
            add_recipe_to_shopping_list(ingredients)

            #Option to save recipe to file
            prompt_save_recipe(recipe)
        else:
            print("Geen passend recept gevonden voor deze weersverwachtingen.")
    else:
        print("ER is een probleem opgetreden met het ophalen van de weer data.")

def print_recipe_details(recipe):
    print(f"Recept: {recipe['label']}")
    print(f"Maaltijdtype: {', '.join(recipe.get('mealType', ['NVT']))}")
    print(f"Gerechtsoort: {', '.join(recipe.get('dishType', ['NVT']))}")
    print(f"Keukentype: {', '.join(recipe.get('cuisineType', ['NVT']))}")
    print(f"Calories: {recipe['calories']:.2f}")
    print(f"URL: {recipe['url']}")

def get_recipe_ingredients(recipe):
    recipe_ingredients = []  # Initialize an empty list to store the ingredients

    # Iterate over each ingredient in the recipe
    for ingredient in recipe['ingredients']:
        food_name = ingredient['food'].lower()
        recipe_ingredients.append(food_name)

    return recipe_ingredients