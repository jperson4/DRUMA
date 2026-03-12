import os

def color(text, color_name):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "black": "\033[30m",
        "bright_red": "\033[91;1m",
        "bright_green": "\033[92;1m",
        "bright_yellow": "\033[93;1m",
        "bright_blue": "\033[94;1m",
        "bright_magenta": "\033[95;1m",
        "bright_cyan": "\033[96;1m",
        "bright_white": "\033[97;1m",
        "gray": "\033[90m",
        "bright_gray": "\033[90;1m",
        "bright_black": "\033[30;1m",
        "orange": "\033[38;5;214m",
        "pink": "\033[38;5;213m",
        "purple": "\033[38;5;129m",
        "lime": "\033[38;5;118m",
        "teal": "\033[38;5;37m",
        "reset": "\033[0m",
    }
    return f"{colors.get(color_name, colors['reset'])}{text}{colors['reset']}"

def clear_terminal():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[2J\033[H", end="")