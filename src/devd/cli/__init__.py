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
    click.secho("Devd ", fg="magenta", bold=True, nl=False)
    click.secho(f"v{__version__}  ", fg="blue", bold=True, nl=False)
    click.secho(f"https://github.com/pateash/devd", fg="green", bold=True, nl=True)


@click.command()
@click.option("--name", help="Say hello to someone", required=False, default="World")
def hello(name):
    click.echo(f"Hello {name}!")


@click.command()
def version():
    click.echo(f"devd v{__version__}")


cli.add_command(hello)
cli.add_command(version)

# implementing this so that if user just uses `devd` we show them something
if __name__ == "devd":
    cli()
