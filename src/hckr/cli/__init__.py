# SPDX-FileCopyrightText: 2024-present Ashish Patel <ashishpatel0720@gmail.com>
#
# SPDX-License-Identifier: MIT
import logging
import time
import webbrowser

import click

from hckr.utils.MessageUtils import warning
from ..__about__ import __version__
from ..cli.cron import cron
from ..cli.crypto import crypto
from ..cli.hash import hash

LOGGING_LEVELS = {
    0: logging.NOTSET,
    # 1: logging.ERROR,
    # 2: logging.WARN,
    1: logging.INFO,
    2: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


# Define a format for the console handler
class Info(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
pass_info = click.make_pass_decorator(Info, ensure=True)


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@click.version_option(version=__version__, prog_name="hckr")
@click.pass_context
@pass_info
def cli(
    _info: Info,
    ctx: click.Context,
    verbose: int,
):
    if verbose > 0:
        logging.basicConfig(
            level=(
                LOGGING_LEVELS[verbose] if verbose in LOGGING_LEVELS else logging.DEBUG
            ),
            format="[%(levelname)s]: %(message)s",
        )
        warning(
            f"Verbose logging (LEVEL={'INFO' if verbose == 1 else 'DEBUG'}) is enabled."
        )
    _info.verbose = verbose
    if ctx.invoked_subcommand is None:
        click.secho("hckr ", fg="magenta", bold=True, nl=False)
        click.secho(f"v{__version__}  ", fg="blue", bold=True, nl=False)
        click.secho(
            f"https://github.com/pateash/hckr\n", fg="green", bold=True, nl=True
        )
        cli(["-h"])


@cli.command(help="Showing Hello message")
@click.option("--name", help="Say hello to someone", required=False, default="World")
def hello(name):
    logging.debug("Hello debug")
    logging.info("Hello info")
    click.secho(f"Hello {name}!", fg="green", nl=True)


@cli.command(help="Showing cli information")
def info():
    click.secho("Version: devd", fg="magenta", bold=True, nl=False)
    click.secho(f"=={__version__}  ", fg="blue", bold=False, nl=True)
    click.secho(
        f"Github: https://github.com/pateash/devd", fg="red", bold=True, nl=True
    )
    click.secho(
        f"PyPi: https://pypi.org/project/devd/", fg="yellow", bold=True, nl=True
    )


@cli.command(help="Opens docs for hckr cli in browser")
def docs():
    url = "https://hckr.readthedocs.io/"
    click.secho("Version: devd", fg="yellow", bold=True, nl=False)
    click.secho(f"=={__version__}  ", fg="blue", bold=False, nl=True)
    click.secho(f"Opening Docs in browser: {url}", fg="red", bold=True, nl=True)
    time.sleep(1)
    webbrowser.open(url)


cli.add_command(cron)
cli.add_command(hash)
cli.add_command(crypto)

# implementing this so that if user just uses `devd` we show them something
if __name__ == "__main__":
    cli()
