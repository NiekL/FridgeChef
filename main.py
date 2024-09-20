import os
from dotenv import load_dotenv

from menu_controller import show_menu
from helper_functions import check_or_create_file, check_or_create_folder

#Load environment variables
load_dotenv()

FRIDGE_FILE = os.getenv("FRIDGE_FILE")
SHOPPING_LIST_FILE = os.getenv("SHOPPING_LIST_FILE")
RECIPE_FOLDER = os.getenv("RECIPES_FOLDER")


def initialize():
    # Check if fridge.csv exist. If not create one in the root directory of the project.
    check_or_create_file(FRIDGE_FILE)

    # Check if shopping_list.csv exist. If not create one in the root directory of the project.
    check_or_create_file(SHOPPING_LIST_FILE)

    # Check if recipes folder exist. If not create one in the root directory of the project.
    check_or_create_folder(RECIPE_FOLDER)


def main():
    """ Main function of FridgeChef. This function starts the application."""
    #Initialize functions to create files and folders
    initialize()

    #Get menu
    show_menu()

if __name__ == "__main__":
    main()