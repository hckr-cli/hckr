import click

from ..utils.MessageUtils import PSuccess
from ..utils.config.ConfigUtils import (
    list_config,
    set_config_value,
)
from ..utils.config.ConfigureUtils import configure_host, configure_creds
from ..utils.config.Constants import (
    CONFIG_TYPE,
    DB_TYPE,
    ConfigType,
    db_type_mapping,
    DB_NAME,
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
    pass


@configure.command("db")
@click.option(
    "--config-name",
    prompt="Enter a name for this database configuration",
    help="Name of the config instance",
)
@click.option(
    "--database-type",
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
@click.option("--database-name", prompt=False, help="Database name")
@click.option("--schema", prompt=False, help="Database schema")
@click.option("--account", prompt=False, help="Snowflake Account Id")
@click.option("--warehouse", prompt=False, help="Snowflake warehouse")
@click.option("--role", prompt=False, help="Snowflake role")
def configure_db(
    config_name,
    database_type,
    host,
    port,
    user,
    password,
    database_name,
    schema,
    account,
    warehouse,
    role,
):
    """Configure database credentials based on the selected database type."""

    set_config_value(config_name, CONFIG_TYPE, ConfigType.DATABASE)
    selected_db_type = db_type_mapping[database_type]
    set_config_value(config_name, DB_TYPE, selected_db_type)

    configure_creds(config_name, password, selected_db_type, user)

    if not database_name:
        database_name = click.prompt("Enter the database name")
    set_config_value(config_name, DB_NAME, database_name)

    configure_host(
        account, config_name, host, port, role, schema, selected_db_type, warehouse
    )

    PSuccess(
        f"Database configuration saved successfully in config instance '{config_name}'"
    )
    list_config(config_name)
