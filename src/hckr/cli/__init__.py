# SPDX-FileCopyrightText: 2024-present Ashish Patel <ashishpatel0720@gmail.com>
#
# SPDX-License-Identifier: MIT
import logging

import click

from hckr.cli.crypto.fernet import fernet
from hckr.cli.info import info
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
class Info:
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
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Enable verbose output, use -v for INFO and -vv for DEBUG",
)
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
            level=(LOGGING_LEVELS.get(verbose, logging.DEBUG)),
            format="[%(levelname)s]: %(message)s",
        )
        warning(
            f"Verbose logging (LEVEL={'INFO' if verbose == 1 else 'DEBUG'}) is enabled. "
            "Use -v for INFO, -vv for DEBUG logs"
        )
    _info.verbose = verbose
    if ctx.invoked_subcommand is None:
        click.secho("hckr ", fg="magenta", bold=True, nl=False)
        click.secho(f"v{__version__}  ", fg="blue", bold=True, nl=False)
        click.secho(
            f"https://github.com/pateash/hckr\n", fg="green", bold=True, nl=True
        )
        cli(["-h"])


cli.add_command(info)
cli.add_command(cron)
cli.add_command(hash)

# we have to add these here otherwise it will be circular imports
# CRYPTO
cli.add_command(crypto)
crypto.add_command(fernet)

# implementing this so that if user just uses `hckr` we show them something
if __name__ == "__main__":
    cli()
