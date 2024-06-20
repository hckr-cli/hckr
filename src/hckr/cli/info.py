import logging
import time
import webbrowser

import click

from ..__about__ import __version__


@click.group(
    help="info commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def info():
    pass


# NOTE - keep command() empty to provide docstr
@info.command()
@click.option("--name", help="Say hello to someone", required=False, default="World")
def hello(name):
    """
    Greets a person with the given name.

    This command outputs a greeting message to the person specified by the `name` option.

    **Example Usage**:

    * Say hello

    .. code-block:: shell

        $ hckr info hello
        Hello World!

    * Say hello to *Alice*

    .. code-block:: shell

        $ hckr info hello --name Alice
        Hello Alice!

    **Command Reference**:
    """
    logging.debug("Hello debug")
    logging.info("Hello info")
    click.secho(f"Hello {name}!", fg="green", nl=True)


@info.command()
def version():
    """
    Show information for CLI and useful links.

    **Example usage**:

    .. code-block:: shell

        $ hckr info version
        Version: devd==VERSION
        Github: https://github.com/pateash/devd
        PyPi: https://pypi.org/project/devd/

    **Command Reference**:
    """
    click.secho("Version: devd", fg="magenta", bold=True, nl=False)
    click.secho(f"=={__version__}  ", fg="blue", bold=False, nl=True)
    click.secho(
        f"Github: https://github.com/pateash/devd", fg="red", bold=True, nl=True
    )
    click.secho(
        f"PyPi: https://pypi.org/project/devd/", fg="yellow", bold=True, nl=True
    )


@info.command(help="Opens docs for hckr cli in browser")
def docs():
    url = "https://hckr.readthedocs.io/"
    click.secho("Version: devd", fg="yellow", bold=True, nl=False)
    click.secho(f"=={__version__}  ", fg="blue", bold=False, nl=True)
    click.secho(f"Opening Docs in browser: {url}", fg="red", bold=True, nl=True)
    time.sleep(1)
    webbrowser.open(url)
