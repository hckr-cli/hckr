import click

from hckr.utils.MessageUtils import success, error
from hckr.utils.TimeUtils import current_time, convert, display


DEFAULT_FORMAT = "%d %B %Y, %I:%M:%S %p %Z"


@click.group(
    help="datetime utilities",
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.argument("date", required=False)
@click.option(
    "-d",
    "--date",
    "date_opt",
    help="Datetime input string, default: Current Datetime, could also be passed through argument",
)
@click.option(
    "-f",
    "--format",
    "fmt",
    default=DEFAULT_FORMAT,
    show_default=True,
    help="Datetime format",
)
@click.option(
    "-z",
    "--timezone",
    "timezone",
    help="Timezone for Datetime parsing",
)
@click.pass_context
def dt(ctx, date, date_opt, fmt, timezone):
    if ctx.invoked_subcommand is not None:
        return
    output = display(date_opt or date, fmt, timezone)
    success(output)


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
