import os
import csv

def show_title_text(title):
    """Simple title function to make the console/menu a little more readable"""
    border = "*" * 25
    title = title.upper()
    print('\n' + border)
    # Center title within 23 (and two '-') characters
    print(f"-\033[92m{title:^23}\033[0m-")
    print(border + '\n')


def colored_text(text, color='green'):
    """Display colored text based on the color parameter."""
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'cyan': '\033[96m',
        'yellow': '\033[93m',
        'magenta': '\033[95m'
    }
    reset = '\033[0m'

    # Get the color code from the dictionary, default to green if not found
    color_code = colors.get(color.lower(), '\033[92m')
    print(f"{color_code}{text}{reset}")


def colored_input(prompt_text, color='magenta'):
    """Display a prompt in a specific color and return the user input."""
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'cyan': '\033[96m',
        'yellow': '\033[93m',
        'magenta': '\033[95m'
    }
    reset = '\033[0m'

    # Get the color code from the dictionary, default to green if not found
    color_code = colors.get(color.lower(), '\033[92m')

    # Display the colored prompt and return the user's input
    return input(f"{color_code}{prompt_text}{reset}")


#------------------------------------------
# Folder/file functions
#------------------------------------------

def check_or_create_folder(folder_name):
    """Check and create the recipes folder if it doesn't exist"""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def check_or_create_file(file_name):
    """Check if the shopping_list.csv file exists, create it if it does not."""
    shopping_list_dir = os.path.dirname(file_name)
    if not os.path.exists(shopping_list_dir):
        os.makedirs(shopping_list_dir)

    if not os.path.isfile(file_name):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['product_name'])
        # print(f"{file_name} is aangemaakt.")
    # else:
    #     print(f"{file_name} bestaat al.")