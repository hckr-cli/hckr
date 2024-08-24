import click
import rich
import speedtest  # type: ignore
from rich.panel import Panel
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from yaspin import yaspin  # type: ignore

from hckr.cli.configure import common_config_options
from hckr.utils import NetUtils, MessageUtils
from hckr.utils.DbUtils import get_db_url
from hckr.utils.NetUtils import get_ip_addresses


@click.group(
    help="Database commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def db():
    pass


@db.command()
@common_config_options
@click.argument('query')
@click.pass_context
def query(ctx, config, query):
    """Execute a SQL query."""
    db_url = get_db_url(section=config)
    if db_url:
        engine = create_engine(db_url)
        try:
            with engine.connect() as connection:
                result = connection.execute(text(query))
                for row in result:
                    click.echo(row)
        except SQLAlchemyError as e:
            click.echo(f"Error executing query: {e}", err=True)
    else:
        click.echo("Database credentials are not properly configured.", err=True)
