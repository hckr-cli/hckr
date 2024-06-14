# SPDX-FileCopyrightText: 2024-present Ashish Patel <ashishpatel0720@gmail.com>
#
# SPDX-License-Identifier: MIT
import click
from rich import print
from ..cli.cron import cron
from ..cli.hash import hash
from ..__about__ import __version__


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="hckr")
@click.pass_context
def cli(ctx: click.Context):
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


cli.add_command(cron)
cli.add_command(hash)

# implementing this so that if user just uses `devd` we show them something
if __name__ == "__main__":
    cli()
