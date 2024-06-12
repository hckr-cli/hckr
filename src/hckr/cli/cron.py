import subprocess
from datetime import datetime, timezone

import click
import rich
from apscheduler.schedulers.blocking import BlockingScheduler  # type: ignore
from apscheduler.triggers.cron import CronTrigger  # type: ignore
from cron_descriptor import get_description  # type: ignore
import time
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
@click.option(
    "-c", "--cmd", help="Command to run as per cron expression", required=True
)
@cron.command(help="run a command using given cron expression")
def run(expr, cmd):
    def run_progress_bar(duration):
        """
        Run a progress bar for the specified duration in seconds.
        """
        with click.progressbar(length=duration, label="Next job will run in") as bar:
            step = 2
            for i in range(0, duration, step):
                time.sleep(step)  # Sleep for a second
                bar.update(step)  # Update the progress bar by one step

    def calculate_sleep_duration(cron_expression):
        # Create a cron iterator based on the cron expression and the current time
        now = datetime.now()
        from croniter import croniter

        cron = croniter(cron_expression, now)
        if not cron.is_valid(cron_expression) or len(cron_expression.split(" ")) != 5:
            error(
                f"Invalid cron Expression: {cron_expression}\n cron expression must have 5 places"
            )
            exit(1)
        # Get the next scheduled time
        next_time = cron.get_next(datetime)
        # Calculate the duration in seconds between now and the next scheduled time
        duration_seconds = (next_time - now).total_seconds()
        return round(duration_seconds)

    try:
        description = get_description(expr)
        info(
            f"Running command: {colored(cmd, 'yellow')}, {colored(description, 'blue')}"
        )

        while True:
            sleep_duration = calculate_sleep_duration(expr)
            run_progress_bar(sleep_duration)
            result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
            success("Output:\n" + ("-" * 50))
            rich.print(result.stdout)
            # Check if the command was successful
            if result.returncode == 0:
                success(("-" * 50))
            else:
                raise Exception("Error in command execution")
    except Exception as e:
        error(f"Error occured:\n {e}")
