from .. import cli
import click
from cron_descriptor import get_description
from rich import print
from ..utils.Message import *


@click.group(
    help="cron related utiltities",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def cron():
    pass


@click.option("-e", "--expr", help="Cron expression", required=True)
@cron.command(help="describe the cron command in human readable terms")
def desc(expr):
    click.echo(f"Describing cron expression: {expr}")
    try:
        description = get_description(expr)
        success(description)
    except Exception as e:
        error(f"Invalid cron expression\n {e}")


@click.option("-e", "--expr", help="Cron expression", required=True)
@cron.command(help="run a command using given cron expression")
def run(expr):
    pass
