import logging

import click
import rich
from rich import print
import random

from rich.panel import Panel


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


def _PMsg(msg, title, desc=None):
    if desc:
        title = f"{title}: {desc}"

    # click.echo("\n")
    rich.print(
        Panel(
            msg,
            expand=True,
            title=title,
        )
    )


def PWarn(msg, title="[yellow]Warning", desc=None):
    _PMsg(msg, title, desc)


def PSuccess(msg, desc=None, title="[green]Success[/green]"):
    _PMsg(msg, title, desc)


def PInfo(msg, desc=None, title="[blue]Info"):
    _PMsg(msg, title, desc)


def PError(msg, desc=None, title="[red]Error"):
    _PMsg(msg, title, desc)
    exit(1)


def info(msg, color=None):
    if color:
        print(f"{info_emoji()} [bold {color}] {msg}[/bold {color}]")
    else:
        print(f"{info_emoji()} [bold blue] {msg}[/bold blue]")


def info_emoji():
    # emoji = random.choice(["information", "slightly_smiling_face", "smiley_cat"])
    emoji = random.choice(["information"])
    return f":{emoji}:"


def success_emoji():
    emoji = random.choice(
        # ["sparkles", "money_with_wings", "white_check_mark", "party_popper", "tada"]
        ["white_check_mark"]
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
