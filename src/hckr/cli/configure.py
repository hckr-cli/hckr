import click

from ..utils import MessageUtils
from ..utils.ConfigUtils import (
    list_config,
    set_config_value,
    db_type_mapping,
    DBType, ConfigType,
)
from ..utils.MessageUtils import PSuccess


@click.group(
    help="easy configurations for other commands (eg. db)",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.pass_context
def configure(ctx):
    """
    Defines a command group for configuration-related commands.
    """
    pass


@configure.command("db")
@click.option(
    "--config_name",
    prompt="Enter a name for this database configuration",
    help="Name of the config instance",
)
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
    prompt=False,  # we will get this value later if it is not provided
    hide_input=True,
    confirmation_prompt=True,
    help="Database password",
)
@click.option("--dbname", prompt=False, help="Database name")
@click.option("--schema", prompt=False, help="Database schema")
@click.option("--account", prompt=False, help="Snowflake Account Id")
@click.option("--warehouse", prompt=False, help="Snowflake warehouse")
@click.option("--role", prompt=False, help="Snowflake role")
def configure_db(
    config_name, db_type, host, port, user, password, dbname, schema, warehouse, role
):
    """Configure database credentials based on the selected database type."""
    set_config_value(config_name, "config_type", ConfigType.DATABASE)
    selected_db_type = db_type_mapping[db_type]
    set_config_value(config_name, "database_type", selected_db_type)

    if selected_db_type in [DBType.PostgreSQL, DBType.MySQL]:
        if not host:
            host = click.prompt("Enter the database host (e.g., localhost, 127.0.0.1)")
        if not port:
            port = click.prompt("Enter the database port (e.g., 5432 for PostgreSQL)")
        if not user:
            user = click.prompt("Enter the database user (e.g., root)")
        if not password:
            password = click.prompt(
                "Enter the database password (input hidden)",
                hide_input=True,
                confirmation_prompt=True,
            )

        set_config_value(config_name, "host", host)
        set_config_value(config_name, "port", port)
        set_config_value(config_name, "user", user)
        set_config_value(config_name, "password", password)
        set_config_value(config_name, "dbname", dbname)

    elif selected_db_type == DBType.SQLite:
        if not dbname:
            dbname = click.prompt("Enter the path to the SQLite database file")
        set_config_value(config_name, "dbname", dbname)

    elif selected_db_type == DBType.Snowflake:
        if not user:
            user = click.prompt("Enter your Snowflake username")
        if not password:
            password = click.prompt(
                "Enter your Snowflake password",
                hide_input=True,
                confirmation_prompt=True,
            )
        if not dbname:
            dbname = click.prompt("Enter the Snowflake database name")
        if not schema:
            schema = click.prompt("Enter the Snowflake schema name")
        if not warehouse:
            warehouse = click.prompt("Enter the Snowflake warehouse name")
        if not role:
            role = click.prompt("Enter the Snowflake role")

        set_config_value(config_name, "user", user)
        set_config_value(config_name, "password", password)
        set_config_value(config_name, "account", account)
        set_config_value(config_name, "warehouse", warehouse)
        set_config_value(config_name, "dbname", dbname)
        set_config_value(config_name, "schema", schema)
        set_config_value(config_name, "role", role)

    PSuccess(
        f"Database configuration saved successfully in config instance '{config_name}'"
    )
    list_config(config_name)
