import os
import re

import click

from . import MessageUtils
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
                 , title=f"Listing [green][{len(env_vars)}][/green] Environment Variables")


def _check_current_shell(shell):
    """Determine the current shell."""
    current_shell = os.path.basename(os.environ.get('SHELL'))

    if shell != current_shell:
        PError(
            f"Looks like you are currently using [yellow]{current_shell}[/yellow]\n but your config is set [yellow][DEFAULT] shell_type = {shell}[/yellow].\n"
            f" Please either pass -s/--shell option to provide shell type manually \n"
            f" or edit config file [magenta]{config_path}[/magenta] using "
            f"[green]hckr config set shell_type <shell_type>")


def set_env(var_name, value, shell=None):
    """Set an environment variable permanently."""
    home = os.path.expanduser("~")

    if shell is None:
        MessageUtils.info(f"Shell is not provided trying to get from {config_path} file")
        shell = ConfigUtils.get_config_value(DEFAULT_CONFIG, 'shell_type')
        _check_current_shell(shell) # user must be using same type of shell to run this command
        MessageUtils.info(f"Got shell as {shell} from config file")

    if shell == 'bash':
        profile = os.path.join(home, '.bashrc')
    elif shell == 'zsh':
        profile = os.path.join(home, '.zshrc')
    else:
        PError("Invalid shell. Try bash or zsh")

    with open(profile, 'a') as file:
        file.write(f'\nexport {var_name}="{value}"\n')

    PSuccess(f'[magenta]{var_name}[/magenta] <- [yellow]{value}[/yellow]',
             f'Value set and sourced in [yellow]{profile}')
    MessageUtils.success(f"Please run [yellow]source {profile}[/yellow] to apply changes")
