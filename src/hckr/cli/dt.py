from datetime import datetime

import click
import humanize
import pytz
from dateutil import parser
from yaspin import yaspin  # type: ignore

from hckr.utils.MessageUtils import PSuccess


@click.group(
    help="datetime commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def dt():
    pass


@dt.command()
@click.argument('date', required=False, default=datetime.now())
@click.option('-f', '--format', 'date_format', default="DD MMMM YYYY, h:mm:ss A, Z UTC",
              help="Datetime format, default: 'Do MMMM YYYY, h:mm:ss A, Z UTC'.")
@click.option('-z', '--timezone', 'timezone', default=pytz.timezone('UTC'),
              help="Timezone for Datetime parsing, default: UTC.")
@click.pass_context
def desc(ctx, date, date_format, timezone):
    """Describe """
    # Parse the date, use current time if not provided
    parsed_date = parser.parse(date)

    # Set timezone
    tz = pytz.timezone(timezone) if isinstance(timezone, str) else timezone
    dt_tz = parsed_date.astimezone(tz)

    # Format the date
    formatted_date = dt_tz.strftime(date_format)

    # Human-readable date
    human_readable = humanize.naturaltime(dt_tz)
    PSuccess(f"Formatted Date: {formatted_date}\nHuman-readable: {human_readable}\n{dt_tz}")
