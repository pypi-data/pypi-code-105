from colorama import Fore, Style


def color(message, color):
    color = Style.BRIGHT + getattr(Fore, color.upper())
    return color + message + Style.NORMAL + Fore.RESET


def print_general_error_message(message):
    print("An unknown error has occurred.")
    print("Details: " + color(message, 'MAGENTA'))
