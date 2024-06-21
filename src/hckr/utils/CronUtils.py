import time
from datetime import datetime

import click
from croniter import croniter
from rich.progress import track

from hckr.utils.MessageUtils import error


def _get_step(duration):
    if duration < 5:
        step = 1
    elif duration < 20:
        step = 2
    else:
        step = 5
    return step


def run_progress_bar(duration):
    """
    Run a progress bar for the specified duration in seconds.
    """
    step = _get_step(duration)
    with click.progressbar(length=duration, label="Next job will run in") as bar:
        for i in range(0, duration, step):
            time.sleep(step)  # Sleep for a second
            bar.update(step)  # Update the progress bar by one step


# Using Rich's progress bar
def run_progress_barV2(duration):
    """
    Run a progress bar for the specified duration in seconds.
    """
    step = _get_step(duration)
    for _ in track(range(0, duration, step), description="[blue]Next job will run in"):
        time.sleep(step)  # Sleep for a second


def calculate_sleep_duration(cron_expression):
    # Create a cron iterator based on the cron expression and the current time
    now = datetime.now()

    cron = croniter(cron_expression, now)
    if not cron.is_valid(cron_expression):
        error(f"Invalid cron Expression: {cron_expression}")
        exit(1)
    if len(cron_expression.split(" ")) != 5:
        error(
            f"Invalid cron Expression: {cron_expression}\n cron expression must have 5 places"
        )
        exit(1)
    # Get the next scheduled time
    next_time = cron.get_next(datetime)
    # Calculate the duration in seconds between now and the next scheduled time
    duration_seconds = (next_time - now).total_seconds()
    return round(duration_seconds)
