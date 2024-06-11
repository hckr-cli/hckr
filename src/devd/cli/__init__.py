# SPDX-FileCopyrightText: 2024-present Ashish Patel <ashishpatel0720@gmail.com>
#
# SPDX-License-Identifier: MIT
import click

from ..__about__ import __version__


# @click.group(
#     context_settings={"help_option_names": ["-h", "--help"]},
#     invoke_without_command=True,
# )
# @click.version_option(version=__version__, prog_name="devd")
# def cli():
#     pass


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="Devd")
@click.pass_context
def cli(ctx: click.Context):
    if ctx.invoked_subcommand is None: # only devd is used then show help
        click.secho("Devd ", fg="magenta", bold=True, nl=False)
        click.secho(f"v{__version__}  ", fg="blue", bold=True, nl=True)
        cli(["--help"])

@click.command()
@click.option("--name", help="Say hello to someone", required=False, default="World")
def hello(name):
    click.secho(f"Hello {name}!", fg="green", nl=True)


@click.command(help="Showing cli information information")
def info():
    click.secho("Version: devd", fg="magenta", bold=True, nl=False)
    click.secho(f"=={__version__}  ", fg="blue", bold=False, nl=True)
    click.secho(f"Github: https://github.com/pateash/devd", fg="red", bold=True, nl=True)
    click.secho(f"PyPi: https://pypi.org/project/devd/", fg="yellow", bold=True, nl=True)

cli.add_command(hello)
cli.add_command(info)

# implementing this so that if user just uses `devd` we show them something
if __name__ == "__main__":
    cli()
