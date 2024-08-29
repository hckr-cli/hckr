import click
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from hckr.cli.config import common_config_options
from hckr.utils.DataUtils import print_df_as_table
from hckr.utils.DbUtils import get_db_url
from hckr.utils.MessageUtils import PError, PInfo


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
def query(ctx, config, query, num_rows=None, num_cols=None):
    """
    This command executes a SQL query on your configured database and show you result in a table format ( in
    ``SELECT/SHOW/DESC`` queries )

    **Example Usage**:

    * Running a simple query on your configured database

    .. code-block:: shell

        $ hckr db query "select 1 as key, 'one' as value" -c testdb_sqlite

    .. table:: Output
       :widths: auto

       =====    =========
       key      value
       =====    =========
       1        one
       =====    =========


    .. note::
       here, we have configured ``Sqlite`` database with in a config 'testdb_sqlite'
       using :ref:`Configuring your databases <configuration>`


    * Additionally, we can also limit number of records and columns returned by the query using ``-nr/--num-rows`` and ``-nc/--num-cols`` options

    .. code-block:: shell

        $ hckr db query "select 1 as key, 'one' as value" -c testdb_sqlite -nr 1 -nc 1

    **Command Reference**:
    """
    db_url = get_db_url(section=config)
    if not db_url:
        PError("Database credentials are not properly configured.")

    query = query.strip()
    engine = create_engine(db_url)
    try:
        with engine.connect() as connection:
            # Normalize and determine the type of query
            normalized_query = query.lower()
            is_data_returning_query = normalized_query.startswith(
                ("select", "desc", "describe", "show", "explain")
            )
            is_ddl_query = normalized_query.startswith(
                ("create", "alter", "drop", "truncate")
            )

            if is_data_returning_query:
                # Execute and fetch results for queries that return data
                df = pd.read_sql_query(text(query), connection)

                # Optionally limit rows and columns if specified
                if num_rows is not None:
                    df = df.head(num_rows)
                if num_cols is not None:
                    df = df.iloc[:, :num_cols]

                print_df_as_table(df, title=query)
                return df
            else:
                # Execute DDL or non-data-returning DML queries
                with connection.begin():  # this will automatically commit at the end
                    result = connection.execute(text(query))
                if is_ddl_query:
                    PInfo(query, "Success")
                else:
                    PInfo(query, f"[Success] Rows affected: {result.rowcount}")
    except SQLAlchemyError as e:
        PError(f"Error executing query: {e}")
