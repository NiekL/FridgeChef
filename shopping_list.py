import os
import csv
from fridge import get_fridge_contents
from helper_functions import colored_text, colored_input, check_or_create_file

# File path for the shopping list CSV
SHOPPING_LIST_FILE = os.getenv("SHOPPING_LIST_FILE")

def check_or_create_shopping_list_file():
    """Check if the shopping_list.csv file exists, create it if it does not."""
    shopping_list_dir = os.path.dirname(SHOPPING_LIST_FILE)
    if not os.path.exists(shopping_list_dir):
        os.makedirs(shopping_list_dir)

    if not os.path.isfile(SHOPPING_LIST_FILE):
        with open(SHOPPING_LIST_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['product_name'])
        print(f"{SHOPPING_LIST_FILE} is aangemaakt.")
    else:
        print(f"{SHOPPING_LIST_FILE} bestaat al.")


def add_product_to_shopping_list(product_name):
    """Add a product to the shopping list."""
    products = []
    with open(SHOPPING_LIST_FILE, mode='r') as file:
        reader = csv.reader(file)
        products = list(reader)

    #Check if product exists
    product_exists = False
    for row in products:
        if row and row[0] == product_name:
            product_exists = True
            break

    if product_exists:
        print(f"{product_name} staat al op het boodschappenlijstje.")
    else:
        with open(SHOPPING_LIST_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([product_name])
        print(f"{product_name} is toegevoegd aan het boodschappenlijstje.")


def remove_product_from_shopping_list(product_name=None):
    """Remove a product or all products from the shopping list."""
    with open(SHOPPING_LIST_FILE, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader, None)
        product_rows = list(reader)

    if not product_rows:
        print("Het boodschappenlijstje is leeg.")
        return

    if product_name is None:
        confirm = colored_input("Weet je zeker dat je alle producten wilt verwijderen? (ja/nee): ", "magenta").lower()
        if confirm == 'ja':
            with open(SHOPPING_LIST_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)  # Keep the header
            print("Alle product(en) zijn verwijderd van het boodschappenlijstje.")
        else:
            print("Verwijdering geannuleerd.")
    else:
        updated_rows = []
        for row in product_rows:
            if row[0].lower() != product_name.lower():
                updated_rows.append(row)

        if len(updated_rows) == len(product_rows):
            print(f"Het product '{product_name}' is niet gevonden op het boodschappenlijstje.")
        else:
            with open(SHOPPING_LIST_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)  # Write the header again
                writer.writerows(updated_rows)
            print(f"Het product '{product_name}' is verwijderd van het boodschappenlijstje.")



def clear_shopping_list():
    """Clear the entire shopping list after user confirmation."""
    confirm = colored_input("Weet je zeker dat je het boodschappenlijstje wilt legen? (ja/nee): ", "magenta").lower()
    if confirm == 'ja':
        with open(SHOPPING_LIST_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['product_name'])  # Re-create the header after clearing the list
        colored_text("Het boodschappenlijstje is geleegd.", "green")
    else:
        colored_text("Verwijdering geannuleerd.", "red")


def show_shopping_list():
    """Display all the products in the shopping list."""
    print("Producten op het boodschappenlijstje:")
    with open(SHOPPING_LIST_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        product_rows = list(reader)

        if not product_rows:
            print("Het boodschappenlijstje is leeg.")
        for product_row in product_rows:
            if product_row:  # Ensure the row is not empty
                print(f"- {product_row[0]}")


def add_recipe_ingredients_to_shopping_list(ingredients):
    """Add missing ingredients of a recipe to the shopping list."""
    fridge_contents = get_fridge_contents()

    missing_ingredients = []
    for ingredient in ingredients:
        if ingredient.lower() not in fridge_contents:
            missing_ingredients.append(ingredient)

    if missing_ingredients:
        for ingredient in missing_ingredients:
            add_product_to_shopping_list(ingredient)
    else:
        print("Je hebt alle ingrediënten al in huis.")


def check_and_remove_products_in_fridge():
    """Check shopping list against fridge contents and remove products already in the fridge."""
    fridge_contents = get_fridge_contents()

    with open(SHOPPING_LIST_FILE, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader, None)
        shopping_list_items = list(reader)

    if not shopping_list_items:
        print("Het boodschappenlijstje is leeg.")
        return

    # Separate fridge contents into lowercase for comparison using a loop
    fridge_contents_lower = []
    for f in fridge_contents:
        fridge_contents_lower.append(f.lower())

    # Find items that are in both the fridge and the shopping list using a loop
    removed_items = []
    for item in shopping_list_items:
        if item[0].lower() in fridge_contents_lower:
            removed_items.append(item)

    # Keep only the items that are not in the fridge using a loop
    remaining_items = []
    for item in shopping_list_items:
        if item[0].lower() not in fridge_contents_lower:
            remaining_items.append(item)

    # Check if any products were removed
    if removed_items:
        # Ask for confirmation before removing the items
        print("De volgende producten zitten al in de koelkast en kunnen van het boodschappenlijstje worden verwijderd:")
        for item in removed_items:
            print(f"- {item[0]}")

        confirm = colored_input("Wil je deze producten verwijderen van het boodschappenlijstje? (ja/nee): ", "magenta").lower()

        if confirm == 'ja':
            # Rewrite the shopping list with remaining items
            with open(SHOPPING_LIST_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)  # Write the header
                writer.writerows(remaining_items)  # Write the remaining items

            print("De product(en) zijn verwijderd van het boodschappenlijstje.")
        else:
            print("Verwijdering geannuleerd. Geen producten zijn verwijderd.")
    else:
        print("Geen producten uit het boodschappenlijstje zaten al in de koelkast.")
