import os
import re

import click

from .MessageUtils import PError, PInfo, PSuccess, PWarn
from .config import ConfigUtils
from .config.Constants import DEFAULT_CONFIG, config_path


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
        PSuccess("\n".join(
            [f"[magenta]{key}[/magenta] = [yellow]{value}" for key, value in env_vars.items()]
        ) if env_vars.items() else "NOTHING FOUND"
                 ,title=f"Listing [green][{len(env_vars)}][/green] Environment Variables")


def set_env(var_name, value, shell=None):
    """Set an environment variable permanently."""
    home = os.path.expanduser("~")

    if shell is None:
        PInfo(f"Shell is not provided trying to get from {config_path} file")
        shell = ConfigUtils.get_config_value(DEFAULT_CONFIG, 'shell_type')
        PInfo(f"Got shell as {shell} from config file")

    if shell == 'bash':
        profile = os.path.join(home, '.bashrc')
    elif shell == 'zsh':
        profile = os.path.join(home, '.zshrc')
    else:
        PError("Invalid shell. Try bash or zsh")

    with open(profile, 'a') as file:
        file.write(f'\nexport {var_name}="{value}"\n')

    PSuccess(f'{var_name} set to {value} permanently in {profile}.')
