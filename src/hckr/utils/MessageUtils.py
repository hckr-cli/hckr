import logging

from rich import print
import random


def colored(msg, color, bold=True):
    if bold:
        return f"[bold {color}]{msg}[/bold {color}]"
    else:
        return f"[{color}]{msg}[/{color}]"


def success(msg):
    print(f"{success_emoji()} [bold green] {msg}[/bold green]")


def error(msg, color=None):
    if color:
        print(f"{error_emoji()} [bold {color}] {msg}[/bold {color}]")
    else:
        print(f"{error_emoji()} [bold red]{msg}[/bold red]")


def warning(msg, color=None):
    if color:
        print(f"{warn_emoji()} [bold {color}] {msg}[/bold {color}]")
    else:
        print(f"{warn_emoji()} [bold yellow]{msg}[/bold yellow]")


def info(msg, color=None):
    if color:
        print(f"{info_emoji()} [bold {color}] {msg}[/bold {color}]")
    else:
        print(f"{info_emoji()} [bold blue] {msg}[/bold blue]")


def info_emoji():
    emoji = random.choice(["information", "slightly_smiling_face", "smiley_cat"])
    return f":{emoji}:"


def success_emoji():
    emoji = random.choice(
        ["sparkles", "money_with_wings", "white_check_mark", "party_popper", "tada"]
    )
    return f":{emoji}:"


def error_emoji():
    emoji = random.choice(["cross_mark", "face_screaming_in_fear", "scream"])
    return f":{emoji}:"


def warn_emoji():
    emoji = random.choice(["warning", "children_crossing"])
    return f":{emoji}:"


def checkOnlyOnePassed(name1, val1, name2, val2):
    if val1 and val2:
        logging.debug(f"Both values  --{name1} and --{name2} are not None")
        error(f"Please use either --{name1} or --{name2}, can't use both")
        exit(1)
    if not val1 and not val2:
        logging.debug(f"Both values --{name1} and --{name2} are None")
        error(f"Please provide either --{name1} or --{name2}")
        exit(1)
