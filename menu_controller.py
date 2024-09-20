from fridge import show_products_in_fridge, add_grocery_to_fridge, remove_product_from_fridge
from recipes import generate_random_recipe, make_recipe_from_fridge, generate_recipe_based_on_weather
from shopping_list import show_shopping_list, add_product_to_shopping_list, remove_product_from_shopping_list, add_recipe_ingredients_to_shopping_list, clear_shopping_list, check_and_remove_products_in_fridge
from helper_functions import show_title_text, colored_input, colored_text


def show_menu():
    """Menu function to display the complete menu. Basically the whole application is running from here"""
    print("\033[92mWelkom bij FridgeChef!\033[0m")

    # Start navigating through the menus
    navigate_menus()

def navigate_menus():
    """Handles navigation across all the menus"""
    while True:
        # Main menu choices
        main_menu_items = [
            "1 - Koelkast",
            "2 - Recepten",
            "3 - Boodschappenlijstje",
            "x - Programma afsluiten"
        ]
        main_menu_callbacks = {
            '1': get_fridge_menu,
            '2': get_recipe_menu,
            '3': get_shopping_list_menu
        }
        handle_menu("Hoofdmenu", main_menu_items, main_menu_callbacks)
        break  # Exit loop after user chooses to exit

def get_fridge_menu():
    """Displays all the possible fridge options and navigate to the fridge features"""
    fridge_menu_items = [
        "1 - Bekijk koelkast",
        "2 - Koelkast bijvullen",
        "3 - Koelkast legen",
        "x - Terug naar hoofdmenu"
    ]
    fridge_menu_callbacks = {
        '1': show_products_in_fridge,
        '2': add_grocery_to_fridge_prompt,
        '3': remove_grocery_from_fridge_menu
    }
    handle_menu("Koelkast", fridge_menu_items, fridge_menu_callbacks)

def get_recipe_menu():
    """Displays all the possible recipe options and navigate to the recipe features"""
    recipe_menu_items = [
        "1 - Genereer willekeurig recept",
        "2 - Recept op basis van het weer",
        "3 - Recepten op basis van koelkast voorraad",
        "x - Terug naar hoofdmenu"
    ]
    recipe_menu_callbacks = {
        '1': generate_random_recipe,
        '2': generate_recipe_based_on_weather,
        '3': make_recipe_from_fridge
    }
    handle_menu("Recepten", recipe_menu_items, recipe_menu_callbacks)

def get_shopping_list_menu():
    """Displays all the possible shopping list options."""
    shopping_list_menu_items = [
        "1 - Bekijk boodschappenlijstje",
        "2 - Product toevoegen aan boodschappenlijstje",
        "3 - Product verwijderen van boodschappenlijstje",
        "4 - Voeg recept ingrediënten toe aan boodschappenlijstje",
        "5 - Boodschappenlijstje leegmaken",
        "6 - Controleer boodschappenlijstje met producten in koelkast",
        "x - Terug naar hoofdmenu"
    ]
    shopping_list_menu_callbacks = {
        '1': show_shopping_list,
        '2': lambda: add_product_to_shopping_list(input("Voer de productnaam in: ")),
        '3': lambda: remove_product_from_shopping_list(input("Voer de productnaam in: ")),
        '4': lambda: add_recipe_ingredients_to_shopping_list([ing.lower() for ing in input("Voer de ingrediënten in (komma gescheiden): ").split(',')]),
        '5': clear_shopping_list,
        '6': check_and_remove_products_in_fridge

    }
    handle_menu("Boodschappenlijstje", shopping_list_menu_items, shopping_list_menu_callbacks)


def add_grocery_to_fridge_prompt():
    """Prompt the user to add a grocery item to the fridge."""
    colored_text("LET OP: producten moeten in het Engels worden toegevoegd.", "yellow")
    product_name = input("Voer de productnaam in: ")
    if product_name:
        add_grocery_to_fridge(product_name)
    else:
        colored_text("Ongeldige invoer, probeer het opnieuw.", "red")

def remove_grocery_from_fridge_menu():
    """Displays options for removing groceries from the fridge"""
    remove_menu_items = [
        "1 - Specifiek product verwijderen",
        "2 - Alle producten verwijderen",
        "x - Terug naar Koelkast menu"
    ]
    remove_menu_callbacks = {
        '1': lambda: remove_product_from_fridge(input("Voer de productnaam in: ")),
        '2': lambda: remove_product_from_fridge()
    }
    handle_menu("Koelkast legen", remove_menu_items, remove_menu_callbacks)

#------------------------------------------
# General menu handling function
#------------------------------------------

def handle_menu(menu_title, menu_items, menu_callbacks):
    """General function to handle menu input and navigation."""
    while True:
        show_title_text(menu_title)
        show_menu_choices(menu_items)
        user_input = colored_input("\nUw keuze: ", "magenta").lower()

        if user_input in menu_callbacks:
            menu_callbacks[user_input]()
        elif user_input == 'x':
            if menu_title.lower() == "hoofdmenu":
                print("Het programma wordt afgesloten.")
            else:
                print(f"U gaat terug naar het {menu_title.lower()} menu.")
            break
        else:
            colored_text("Ongeldige invoer, probeer het opnieuw.", "red")

#------------------------------------------
# Helper functions
#------------------------------------------

def show_menu_choices(options):
    """Display all the menu choices out of a list of options"""
    print("Maak een keuze uit de onderstaande mogelijkheden")
    for option in options:
        print(option)

