import os
import platform
import shutil
import site
import subprocess
import sys

import click

from ..utils import MessageUtils
from ..utils.EnvUtils import list_env, set_env, get_shell_profile
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
@click.argument('variable_name')
@click.argument('variable_value')
@click.option('--shell', type=click.Choice(['bash', 'zsh']), help='Shell type')
def set(variable_name, variable_value, shell):
    """
    This command adds a new entry to the your environment variables

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
    This command returns value for an environment variable for all available environment variables

    **Example Usage**:

    * Getting a value for GITHUB_USER env variable

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
@click.option('-p', '--pattern', required=False, default='.*')
@click.option('-i', '--ignore-case', is_flag=True, help='Ignore case distinctions.')
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

        $ hckr config show --all

    **Command Reference**:
    """
    MessageUtils.info("Listing all environment variables")
    list_env(pattern, ignore_case)


@env.command()
def python():
    """
    This command show all information about your current python environment

    **Example Usage**:

    .. code-block:: shell

        $ hckr env python


    **Command Reference**:
    """
    # PSuccess(f"Python version: {sys.version}\nPython API version: {sys.api_version}",
    #          title=f"[yellow]Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    lib_paths = ''.join(f'  - {path}\n' for path in sys.path)
    site_package_dirs = ''.join(f'  - {path}\n' for path in site.getsitepackages())
    info = f"""Python Version: {sys.version}
Python Executable: {sys.executable}
Platform Information:
------------------
Platform: {sys.platform}
Python Implementation: {platform.python_implementation()}

Python Library Paths:
---------------------
{lib_paths}
Site-Packages Directories:
--------------------------
{site_package_dirs}
Python Environment Variables:
-----------------------------
PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}
PYTHONHOME: {os.environ.get('PYTHONHOME', 'Not set')}
VIRTUAL_ENV: {os.environ.get('VIRTUAL_ENV', 'Not set')}"""
    PSuccess(info, title=f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")


@env.command()
def java():
    try:
        result = subprocess.run(["java", "-version"], capture_output=True, text=True, check=True)
        PSuccess(result.stderr, title="[yellow]Java")  # Java version information is typically in stderr
    except subprocess.CalledProcessError as e:
        PError(f"Java is not installed or not found in PATH.\n{e}")


@env.command()
def shell():
    shell_path = os.environ.get('SHELL')
    shell_name = os.path.basename(shell_path) if shell_path else 'Unknown'
    PSuccess(f"Current shell: [magenta]{shell_name}[/magenta]\n [yellow]{get_shell_profile()}",
             title=f"Shell [green]\[{shell_name}]")


@env.command()
def node():
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        PSuccess(f"Node.js version: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        PError(f"Node.js is not installed or not found in PATH.\n{e}")


@env.command()
def disk():
    total, used, free = shutil.disk_usage("/")
    info = f"""
Total: {total // (2 ** 30)}
GB
Used: {used // (2 ** 30)}
GB
Free: {free // (2 ** 30)}
GB
"""
    PSuccess(info, title=f"Disk Space [green]\[{total // (2 ** 30)} GB]")
