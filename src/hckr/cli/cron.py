import logging
import subprocess

import rich
from cron_descriptor import get_description  # type: ignore
from rich.panel import Panel
from ..utils.CronUtils import calculate_sleep_duration, run_progress_barV2

# from ..utils.MessageUtils import *
import click
from ..utils.MessageUtils import success, error, info, checkOnlyOnePassed, colored


@click.group(
    help="cron commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def cron():
    pass


@click.option("-e", "--expr", help="Cron expression", required=True)
@cron.command(help="describe the cron command in human readable terms")
def desc(expr):
    info(f"Describing cron expression: {colored(expr, 'magenta')}")
    try:
        description = get_description(expr)
        success(description)
    except Exception as e:
        logging.debug(
            "Some exception occurred while getting description from Croniter."
        )
        error(f"Invalid cron expression\n '{e}'")


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
    checkOnlyOnePassed("seconds", seconds, "expr", expr)
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
