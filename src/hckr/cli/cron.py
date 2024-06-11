import subprocess
from datetime import datetime, timezone

import click
import rich
from apscheduler.schedulers.blocking import BlockingScheduler  # type: ignore
from apscheduler.triggers.cron import CronTrigger  # type: ignore
from cron_descriptor import get_description  # type: ignore

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


# @click.option("-e", "--expr", help="Cron expression", required=True)
# @click.option(
#     "-c", "--cmd", help="Command to run as per cron expression", required=True
# )
# @cron.command(help="run a command using given cron expression")
# def run(expr, cmd):
#     def calculate_sleep_duration(cron_expression):
#         # Create a cron iterator based on the cron expression and the current time
#         now = datetime.now()
#         cron = croniter(cron_expression, now)
#         if not cron.is_valid(cron_expression):
#             error(f"Invalid cron Expression: {cron_expression}")
#             exit(1)
#         # Get the next scheduled time
#         next_time = cron.get_next(datetime)
#         # Calculate the duration in seconds between now and the next scheduled time
#         duration_seconds = (next_time - now).total_seconds()
#         return duration_seconds
#     try:
#         description = get_description(expr)
#         info(f"Running command: {cmd}, {description}")
#
#         while True:
#             sleep_duration = calculate_sleep_duration(expr)
#             info(f'Seconds until next event: {sleep_duration}')
#             time.sleep(sleep_duration)
#             # Example of running a simple ls command
#             result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
#             # Print the output
#             success("Output:")
#             rich.print(result.stdout)
#             # Check if the command was successful
#             if result.returncode == 0:
#                 success("Command executed successfully!")
#             else:
#                 error("Error in command execution.")
#     except Exception as e:
#         error(f"Invalid cron expression\n {e}")


@click.option("-e", "--expr", help="Cron expression", required=True)
@click.option(
    "-c", "--cmd", help="Command to run as per cron expression", required=True
)
@cron.command(help="run a command using given cron expression")
def run(expr, cmd):
    try:

        def my_job(cmd):
            info(f"Running job {cmd}")
            subprocess.run(cmd, shell=True, text=True, capture_output=True)
            output = subprocess.getoutput(cmd)
            rich.print(output)
            rich.print("=" * 50)

        def monitor_scheduler():
            jobs = scheduler.get_jobs()
            if not jobs:
                rich.print("Scheduler is idle with no jobs.")
            else:
                for job in jobs:
                    if ".monitor_scheduler" not in job.name:
                        # print(f"Job '{job.name}', next run at: {job.next_run_time}")
                        time_delta = job.next_run_time - datetime.now(timezone.utc)
                        rich.print(
                            f"Next run in: {round(time_delta.total_seconds())} seconds"
                        )

        description = get_description(expr)
        info(f"Running command: {cmd}, {description}")
        scheduler = BlockingScheduler()
        scheduler.add_job(
            lambda command=cmd: my_job(command), CronTrigger.from_crontab(expr)
        )
        # scheduler.add_job(lambda command=cmd: my_job(command),
        #                   'interval', seconds=5)
        scheduler.add_job(monitor_scheduler, "interval", seconds=5)
        scheduler.start()
    except Exception as e:
        error(f"Invalid cron expression\n {e}")
