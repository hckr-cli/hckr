import click
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from yaspin import yaspin  # type: ignore

from hckr.cli.config import common_config_options
from hckr.utils.DbUtils import get_db_url
from hckr.utils.MessageUtils import PError


@click.group(
    help="Database commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def db():
    pass


@db.command()
@common_config_options
@click.argument("query")
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
            PError(f"Error executing query: {e}")
    else:
        PError("Database credentials are not properly configured.")
