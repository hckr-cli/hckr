import warnings

import click
from sqlalchemy.exc import SAWarning
from yaspin import yaspin  # type: ignore

from hckr.cli.config import common_config_options
from hckr.utils.DbUtils import get_db_url, execute_query
from hckr.utils.MessageUtils import PError

# Suppress the specific SQLAlchemy warning
warnings.filterwarnings("ignore", category=SAWarning, message=".*flatten.*")

# Your SQLAlchemy code


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
def query(ctx, config, config_path, query, num_rows=None, num_cols=None):
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
    db_url = get_db_url(section=config, config_path=config_path)
    if not db_url:
        PError("Database credentials are not properly configured.")
    with yaspin(text="Running query...", color="green", timer=True) as spinner:
        execute_query(db_url, query, num_rows, num_cols)
        spinner.ok("✔")
