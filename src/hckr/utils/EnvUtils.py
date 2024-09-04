import logging
import os
import re

from . import MessageUtils
from .MessageUtils import PError, PSuccess, PWarn


def list_env(pattern, ignore_case):
    """List all environment variables, optionally filtering by a pattern."""

    # Compile the regex pattern
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)

    # Retrieve and filter environment variables
    env_vars = {k: v for k, v in os.environ.items() if regex.search(f"{k}={v}")}

    if not env_vars:
        PWarn("No matching environment variables found.")
        exit(0)
    else:
        PSuccess(
            (
                "\n".join(
                    [
                        f"[magenta]{key}[/magenta] = [yellow]{value}"
                        for key, value in env_vars.items()
                    ]
                )
                if env_vars.items()
                else "NOTHING FOUND"
            ),
            title=f"Listing [green][{len(env_vars)}][/green] Environment Variables",
        )


def get_shell_profile(shell=None):
    if shell is None:
        logging.info("Shell is not provided trying to infer from current shell")
        shell = os.path.basename(os.environ.get("SHELL"))
        MessageUtils.info(f"Inferred from current shell as [yellow]{shell}")
    home = os.path.expanduser("~")

    if shell == "bash":
        profile = os.path.join(home, ".bashrc")
    elif shell == "zsh":
        profile = os.path.join(home, ".zshrc")
    else:
        PError("Invalid shell. Try bash or zsh")
    return profile


def set_env(var_name, value, shell=None):
    """Set an environment variable permanently."""

    profile = get_shell_profile(shell)

    with open(profile, "a") as file:
        file.write(f'\nexport {var_name}="{value}"\n')

    PSuccess(
        f"[magenta]{var_name}[/magenta] <- [yellow]{value}[/yellow]",
        f"Value set and sourced in [yellow]{profile}",
    )
    MessageUtils.success(
        f"Please run [yellow]source {profile}[/yellow] to apply changes"
    )
