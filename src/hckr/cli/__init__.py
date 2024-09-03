# SPDX-FileCopyrightText: 2024-present Ashish Patel <ashishpatel0720@gmail.com>
#
# SPDX-License-Identifier: MIT
import logging

import click
from click_repl import register_repl  # type: ignore

from hckr.cli.db import db
from hckr.cli.configure import configure
from hckr.cli.config import config
from hckr.cli.env import env
from hckr.cli.k8s.context import context
from hckr.cli.k8s.namespace import namespace
from hckr.cli.k8s.pod import pod
from .crypto.fernet import fernet
from .data import data
from .info import info
from .k8s import k8s
from .net import net
from ..__about__ import __version__
from ..cli.cron import cron
from ..cli.crypto import crypto
from ..cli.hash import hash
from ..utils.CliUtils import check_update
from ..utils.MessageUtils import warning

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
            f"https://github.com/hckr-cli/hckr\n", fg="green", bold=True, nl=False
        )
        check_update()
        cli(["-h"])
    else:
        check_update()


register_repl(cli)
cli.add_command(info)
cli.add_command(cron)
cli.add_command(hash)
cli.add_command(data)

# we have to add these here otherwise it will be circular imports
# CRYPTO
cli.add_command(crypto)
crypto.add_command(fernet)

# k8s
cli.add_command(k8s)
k8s.add_command(pod)
k8s.add_command(namespace)
k8s.add_command(context)

# NETWORK command
cli.add_command(net)

# config
cli.add_command(config)
cli.add_command(configure)

# database
cli.add_command(db)

# environment
cli.add_command(env)


# implementing this so that if the user just uses `hckr` we show them something
if __name__ == "__main__":
    cli()
