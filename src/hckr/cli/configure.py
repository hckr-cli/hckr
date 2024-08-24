# from ..utils.MessageUtils import *
import logging

import click
import rich
from cron_descriptor import get_description  # type: ignore
from rich.panel import Panel

from .config import common_config_options
from ..utils import MessageUtils
from ..utils.ConfigUtils import (
    load_config,
    config_path,
    ensure_config_file,
    DEFAULT_CONFIG,
    configMessage,
    list_config,
    set_config_value,
    get_config_value,
    db_type_mapping, DBType,
)


@click.group(
    help="easy configurations for other commands (eg. db)",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.pass_context
def configure(ctx):
    """
    Defines a command group for configuration-related commands.
    """
    ensure_config_file()


# @configure.command("db")
# @click.option(
#     "--config_name",
#     prompt="Enter a name for this database configuration",
#     help="Name of the config instance",
# )
# @click.option(
#     "--db_type",
#     prompt="Select the type of database (1=PostgreSQL, 2=MySQL, 3=SQLite, 4=Snowflake)",
#     type=click.Choice(["1", "2", "3", "4"]),
#     help="Database type",
# )
# @click.option(
#     "--host",
#     prompt="Enter the database host (e.g., localhost, 127.0.0.1)",
#     help="Database host",
# )
# @click.option(
#     "--port", prompt="Enter the database port (e.g., 5432)", help="Database port"
# )
# @click.option(
#     "--user", prompt="Enter the database user (e.g., root)", help="Database user"
# )
# @click.option(
#     "--password",
#     prompt="Enter the database password (input hidden)",
#     hide_input=True,
#     confirmation_prompt=True,
#     help="Database password",
# )
# @click.option("--dbname", prompt="Enter the name of the database", help="Database name")
# def configure_db(config_name, db_type, host, port, user, password, dbname):
#     """Configure database credentials."""
#
#     set_config_value(config_name, "db_type", db_type_mapping[db_type])
#     set_config_value(config_name, "host", host)
#     set_config_value(config_name, "port", port)
#     set_config_value(config_name, "user", user)
#     set_config_value(config_name, "password", password)
#     set_config_value(config_name, "dbname", dbname)
#
#     MessageUtils.success(
#         f"Database configuration saved successfully in config instance '{config_name}'"
#     )
#     list_config(config_name)
#     MessageUtils.success(
#         f"Now you can use config {config_name}, using -c/--config in hckr db commands"
#     )


@configure.command("db")
@click.option("--config_name", prompt="Enter a name for this database configuration",
              help="Name of the config instance")
@click.option(
    "--db_type",
    prompt="Select the type of database (1=PostgreSQL, 2=MySQL, 3=SQLite, 4=Snowflake)",
    type=click.Choice(["1", "2", "3", "4"]),
    help="Database type",
)
@click.option("--host", prompt=False, help="Database host")
@click.option("--port", prompt=False, help="Database port")
@click.option("--user", prompt=False, help="Database user")
@click.option(
    "--password",
    prompt=False,
    hide_input=True,
    confirmation_prompt=True,
    help="Database password",
)
@click.option("--dbname", prompt="Enter the name of the database", help="Database name")
@click.pass_context
def configure_db(ctx, config_name, db_type, host, port, user, password, dbname):
    """Configure database credentials based on the selected database type."""
    selected_db_type = db_type_mapping[db_type]
    # set_config_value(config_name, "db_type", str(selected_db_type))
    set_config_value(config_name, "type", selected_db_type)

    if selected_db_type in [DBType.PostgreSQL, DBType.MySQL, DBType.Snowflake]:
        if not host:
            host = click.prompt("Enter the database host (e.g., localhost, 127.0.0.1)")
        if not port:
            port = click.prompt("Enter the database port (e.g., 5432 for PostgreSQL)")
        if not user:
            user = click.prompt("Enter the database user (e.g., root)")
        if not password:
            password = click.prompt("Enter the database password (input hidden)", hide_input=True,
                                    confirmation_prompt=True)

        set_config_value(config_name, "host", host)
        set_config_value(config_name, "port", port)
        set_config_value(config_name, "user", user)
        set_config_value(config_name, "password", password)

    if selected_db_type == "SQLite":
        # SQLite only requires a database file path
        if not dbname:
            dbname = click.prompt("Enter the path to the SQLite database file")
        set_config_value(config_name, "dbname", dbname)
    else:
        set_config_value(config_name, "dbname", dbname)

    MessageUtils.success(f"Database configuration saved successfully in config instance '{config_name}'")
    list_config(config_name)
