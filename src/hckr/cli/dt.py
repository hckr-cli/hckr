import click

from hckr.utils.MessageUtils import success, error
from hckr.utils.TimeUtils import current_time, convert


@click.group(
    help="datetime utilities",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def dt():
    pass


@dt.command(help="show current time in the given timezone")
@click.option(
    "-t",
    "--timezone",
    default="UTC",
    show_default=True,
    help="Timezone in which to display the time",
)
def now(timezone):
    try:
        dt_now = current_time(timezone)
        success(f"Current time in {timezone}: {dt_now.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception:
        error("Failed to get current time")


@dt.command(help="convert datetime between timezones")
@click.option("--datetime", "dt_str", required=True, help="Datetime in ISO format")
@click.option("--from-tz", required=True, help="Source timezone")
@click.option("--to-tz", required=True, help="Destination timezone")
def convert_time(dt_str, from_tz, to_tz):
    try:
        result = convert(dt_str, from_tz, to_tz)
        success(
            f"{dt_str} [{from_tz}] -> {result.strftime('%Y-%m-%d %H:%M:%S')} [{to_tz}]"
        )
    except Exception:
        error("Failed to convert time")
