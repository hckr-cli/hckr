import os
import platform
import shutil
import site
import subprocess
import sys
import time
import webbrowser

import click

from ..__about__ import __version__
from ..utils import MessageUtils
from ..utils.EnvUtils import get_shell_profile
from ..utils.MessageUtils import error, PSuccess, PError, PInfo


@click.group(
    help="info commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def info():
    pass


@info.command(help="Opens docs for hckr cli in browser")
def docs():
    url = "https://hckr.readthedocs.io/"
    click.secho("Version: hckr", fg="yellow", bold=True, nl=False)
    click.secho(f"=={__version__}  ", fg="blue", bold=False, nl=True)
    click.secho(f"Opening Docs in browser: {url}", fg="red", bold=True, nl=True)
    time.sleep(1)
    try:
        webbrowser.open(url)
    except Exception as e:
        error(f"Some error occured while opening docs in browser\n{e}")


@info.command()
def python():
    """
    This command show all information about your current python environment

    **Example Usage**:

    .. code-block:: shell

        $ hckr info python


    **Command Reference**:
    """
    lib_paths = "".join(f"  - {path}\n" for path in sys.path)
    site_package_dirs = "".join(f"  - {path}\n" for path in site.getsitepackages())
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
    PSuccess(
        info,
        title=f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    )


@info.command()
def java():
    """
    This command show all information about your current java environment

    **Example Usage**:

    .. code-block:: shell

        $ hckr info java


    **Command Reference**:
    """
    try:
        # Java version
        java_version = subprocess.check_output(
            ["java", "-version"], stderr=subprocess.STDOUT, text=True
        ).strip()

        # Java home
        java_home = (
            subprocess.check_output(
                ["echo", "$JAVA_HOME"], shell=True, text=True
            ).strip()
            or "[NOT SET]"
        )

        # Java classpath
        classpath = (
            subprocess.check_output(
                ["echo", "$CLASSPATH"], shell=True, text=True
            ).strip()
            or "[NOT SET]"
        )

        # Java vendor
        java_vendor = subprocess.check_output(
            ["java", "-XshowSettings:properties", "-version"],
            stderr=subprocess.STDOUT,
            text=True,
        )

    except subprocess.CalledProcessError as e:
        return f"Error fetching Java environment information: {e}"

    info = f"""
Java Version:
-------------
{java_version}

Java Home:
----------
{java_home}

Java Classpath:
---------------
{classpath}

Java Vendor and System Properties:
-----------------------------------
{java_vendor}"""

    try:
        PSuccess(
            info, title="[yellow]Java"
        )  # Java version information is typically in stderr
    except subprocess.CalledProcessError as e:
        PError(f"Java is not installed or not found in PATH.\n{e}")


@info.command()
def shell():
    """
    This command show all information about your current shell

    **Example Usage**:

    .. code-block:: shell

        $ hckr info shell


    **Command Reference**:
    """
    shell_path = os.environ.get("SHELL")
    if not shell_path:
        PError(
            "$SHELL variable is not set inside python env, please check if this is available."
        )
    shell_name = os.path.basename(shell_path)
    PSuccess(
        f"Current shell: [magenta]{shell_name}[/magenta]\n [yellow]{get_shell_profile()}",
        title=f"Shell [green]\[{shell_name}]",
    )


@info.command()
def disk():
    """
    This command show all information about your current disk and usage

    **Example Usage**:

    .. code-block:: shell

        $ hckr info disk


    **Command Reference**:
    """
    total, used, free = shutil.disk_usage("/")
    info = f"""Total: {total // (2 ** 30)} GB
[yellow]Used:{used // (2 ** 30)} GB[/yellow]
[green]Free:{free // (2 ** 30)} GB [/green]"""
    PSuccess(info, title=f"Disk Space [green]\[{total // (2 ** 30)} GB free]")


# @info.command()
# def version():
#     """
#     Show information for Hckr CLI and useful links.
#
#     **Example usage**:
#
#     .. code-block:: shell
#
#         $ hckr info version
#         Version: hckr==VERSION
#         Github: https://github.com/hckr-cli/hckr
#         PyPi: https://pypi.org/project/hckr/
#
#     **Command Reference**:
#     """
#     click.secho("Version: hckr", fg="magenta", bold=True, nl=False)
#     click.secho(f"=={__version__}  ", fg="blue", bold=False, nl=True)
#     check_update(show_no_update=True)
#     click.secho(
#         f"Github: https://github.com/hckr-cli/hckr", fg="red", bold=True, nl=True
#     )
#     click.secho(
#         f"PyPi: https://pypi.org/project/hckr/", fg="yellow", bold=True, nl=True
#     )
