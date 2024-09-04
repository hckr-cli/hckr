import os

import click

from ..utils import MessageUtils
from ..utils.EnvUtils import list_env, set_env
from ..utils.MessageUtils import PSuccess, PError


@click.group(
    help="Environment commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def env():
    """
    Defines a command group for managing environment variables
    """
    pass


@env.command()
@click.argument("variable_name")
@click.argument("variable_value")
@click.option("--shell", type=click.Choice(["bash", "zsh"]), help="Shell type")
def set(variable_name, variable_value, shell):
    """
    This command adds a new entry to your environment variables by updating your profile ( ~/.zshrc or ~/.bashrc etc.)

    **Example Usage**:

    * Setting an environment variable in your current shell profile ( ~/.zshrc or ~/.bashrc )


    .. code-block:: shell

        $ hckr env set GITHUB_USER pateash

    .. info::
       this will add an entry in your profile ( ~/.zshrc or ~/.bashrc ) with
       export GITHUB_USER="pateash"

        We will need to source ``.bashrc / .zshrc`` to apply changes.

    .. tip::
       By default when we run this command it will infer shell type from current shell.
       for writing it inside different shell profile either you can pass it as an option using ``-s / --shell`` as shown below.

    * If We want to provide shell type explicitly, we can use ``-s/--shell option``

    .. code-block:: shell

        $ hckr env set GITHUB_USER pateash --shell bash

    **Command Reference**:
    """
    set_env(variable_name, variable_value, shell)


@env.command()
@click.argument("variable")
def get(variable):
    """
    This command returns value for an environment variable from all available environment variables

    **Example Usage**:

    * Getting a value for GITHUB_USER env variable

    .. tip::
       If your environment variable is not set you will get an ``error`` message.

    .. code-block:: shell

        $ hckr env get GITHUB_USER


    **Command Reference**:
    """
    value = os.environ.get(variable)
    if value is None:
        PError(f"Environment variable '{variable}' is not set.")
    else:
        PSuccess(f"[magenta]{variable}[/magenta] = [green]{value}")


@env.command("list")
@click.option("-p", "--pattern", required=False, default=".*")
@click.option("-i", "--ignore-case", is_flag=True, help="Ignore case distinctions.")
def env_list(pattern, ignore_case):
    """
    This command show list all environment variables, we can also filter them by regex pattern using ``-p/--pattern`` option
    and we can also apply to ignore cases of a pattern using ``-i/--ignore-case`` option

    **Example Usage**:

    * Listing all Environment variables

    .. code-block:: shell

        $ hckr env list

    * Similarly, We can filter the environment vars with ``-p/--pattern`` option

    .. code-block:: shell

        $ hckr env list -p 'PYENV'

    * Additionally, We can also allow ignoring case filters using ``-i/--ignore-case`` option

    .. code-block:: shell

        $ hckr config list --all

    **Command Reference**:
    """
    MessageUtils.info("Listing all environment variables")
    list_env(pattern, ignore_case)
