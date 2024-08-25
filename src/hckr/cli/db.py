import click
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from yaspin import yaspin  # type: ignore

from hckr.cli.config import common_config_options
from hckr.utils.ConfigUtils import config_path
from hckr.utils.DataUtils import print_df_as_table
from hckr.utils.DbUtils import get_db_url
from hckr.utils.MessageUtils import PError
import pandas as pd

@click.group(
    help="Database commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def db():
    pass


@db.command()
@common_config_options
@click.argument("query")
@click.option(
    "-nr",
    "--num-rows",
    default=10,
    help="Number of rows to show.",
    required=False,
)
@click.option(
    "-nc",
    "--num-cols",
    default=10,
    help="Number of cols to show.",
    required=False,
)
@click.pass_context
def query(ctx, config, query, num_rows, num_cols):
    """Execute a SQL query on Snowflake and return a DataFrame."""
    db_url = get_db_url(section=config)

    if db_url:
        engine = create_engine(db_url)
        try:
            with engine.connect() as connection:
                # Execute the query and convert the result to a DataFrame
                df = pd.read_sql_query(text(query), connection)
                print_df_as_table(df, title=query, count=num_rows, col_count=num_cols)
        except SQLAlchemyError as e:
            PError(f"Error executing query: {e}")
    else:
        PError("Database credentials are not properly configured.")
