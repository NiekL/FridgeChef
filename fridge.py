import os
import csv

from helper_functions import colored_text, colored_input

from dotenv import load_dotenv

load_dotenv()

# File path for the fridge CSV
FRIDGE_FILE = os.getenv("FRIDGE_FILE")

#------------------------------------------
# Fridge general functions
#------------------------------------------

def add_grocery_to_fridge(name):
    """Add a grocery item to the fridge.csv file."""
    groceries = []

    # Read the file to see if the product exists
    with open(FRIDGE_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        groceries = list(reader)  # Convert reader object to a list

    # Check if the product exists
    product_exists = any(row and row[0] == name for row in groceries)

    if product_exists:
        print(f"{name} is already in the fridge.")
    else:
        # If product doesn't exist, append it using 'a' mode
        with open(FRIDGE_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name.lower()])
        print(f"{name} is toegevoegd aan de koelkast.")

    back_to_menu()

def remove_product_from_fridge(product_name=None):
    """
    Remove a specific product from the fridge.csv file or remove all products.

    Args:
        product_name (str): The name of the product to remove. If None, all products will be removed.
    """
    with open(FRIDGE_FILE, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader, None)
        product_rows = list(reader)

    if not product_rows:
        print("De koelkast is al leeg.")
        return

    if product_name is None:
        # Remove all products
        confirm = colored_input("Weet je zeker dat je alle producten wilt verwijderen? (ja/nee): ", "magenta").lower()
        if confirm == 'ja':
            with open(FRIDGE_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)  # Keep the header, but clear the content
            print("Alle product(en) zijn verwijderd.")
        else:
            print("Verwijdering geannuleerd.")
    else:
        # Remove a specific product
        updated_rows = [row for row in product_rows if row[0].lower() != product_name.lower()]

        if len(updated_rows) == len(product_rows):
            print(f"Het product '{product_name}' is niet gevonden in de koelkast.")
        else:
            with open(FRIDGE_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)  # Write the header again
                writer.writerows(updated_rows)  # Write the remaining products
            print(f"Het product '{product_name}' is verwijderd.")

    back_to_menu()

def show_products_in_fridge():
    """Display all the products in the fridge.csv file."""
    print("Producten in de koelkast:")

    with open(FRIDGE_FILE, mode='r') as file:
        reader = csv.reader(file)

        # Read the header
        header = next(reader, None)

        # Check if the file is empty or only contains the header
        product_rows = list(reader)
        if not product_rows:
            print("De koelkast is leeg.")
        # Display the products
        for product_row in product_rows:
            if product_row:  # Ensure the row is not empty
                print(f"- {product_row[0]}")

        back_to_menu()

def get_fridge_contents():
    """Return a list of products currently in the fridge."""
    with open(FRIDGE_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        products = []
        # Collect and clean product names from each row
        for row in reader:
            if row:  # Ensure row is not empty
                product_name = row[0].strip()
                products.append(product_name)

    return products


def back_to_menu():
    """Go back to the Fridge menu."""
    while True:
        go_back = colored_input("\nTyp x om terug te gaan naar het vorige menu: ", "magenta")
        if go_back.lower() == "x":
            break
        else:
            colored_text("Ongeldige invoer, probeer het opnieuw.", "red")
            continue
