import subprocess

import rich
from cron_descriptor import get_description  # type: ignore
from hckr.utils.CronUtils import *
from rich.panel import Panel

from ..utils.MessageUtils import *


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


@click.option(
    "-c", "--cmd", help="Command to run as per cron expression", required=True
)
@click.option("-e", "--expr", help="Cron expression", required=False, default=None)
@click.option(
    "-s",
    "--seconds",
    help="Interval in number of seconds to run command",
    required=False,
    default=None,
)
@click.option(
    "-t",
    "--timeout",
    help="Max number of times this command should run",
    required=False,
    default=100,
)
@cron.command(help="run a command using given cron expression")
def run(cmd, expr, seconds, timeout):
    if seconds and expr:
        error("Please use either --expr or --seconds to pass schedule, can't use both")
        exit(1)
    if not seconds and not expr:
        error("Please provide either --expr or --seconds to pass schedule")
        exit(1)
    try:
        if expr:
            description = get_description(expr)
            info(
                f"Running command: {colored(cmd, 'yellow')}, {colored(description, 'blue')}"
            )
        elif seconds:
            info(
                f"Running command: {colored(cmd, 'yellow')}, {colored(f'Every {seconds} seconds', 'blue')}"
            )
        i = 1
        while i <= timeout:
            result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
            if result.returncode != 0:
                raise Exception(f"Error in command execution {result.stderr}")
            rich.print(
                Panel(
                    result.stdout,
                    expand=True,
                    subtitle="End",
                    title=f"Output [{i}/{timeout}]",
                )
            )
            # rich.print(result.stdout)
            sleep_duration = calculate_sleep_duration(expr) if expr else int(seconds)
            run_progress_barV2(sleep_duration)
            i += 1
    except Exception as e:
        error(f"{e}")
        # raise e
