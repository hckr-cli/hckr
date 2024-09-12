import click

from ..utils.MessageUtils import PSuccess
from ..utils.config.ConfigUtils import (
    list_config,
    set_config_value,
    set_default_config,
    config_file_path_option,
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
    help="Easy configurations for other commands (eg. db)",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.pass_context
def configure(ctx):
    """
    Defines a command group for configuration-related commands.
    """
    pass


@configure.command()
@config_file_path_option
@click.argument("service", type=click.Choice([str(ConfigType.DATABASE)]))
@click.argument("config_name")
def set_default(service, config_name, config_path):
    """Set the default configuration for a service configured via ``hckr configure``
    This command configures database credentials based on the selected database type.

    .. hint::
       We currently support ``database`` default configuration which corresponds to ``hckr configure``,

    **Example Usage**:

    * Setting up your default database configuration in [DEFAULT] configuration


    .. code-block:: shell

        $ hckr configure set-default db MY_DB_CONFIG

    .. note::
       Please note that the ``MY_DB_CONFIG`` config must be configured before running this using ``hckr configure db`` command

    .. important:: This command will add an entry in ``[DEFAULT]`` configuration like ``database = MY_DB_CONFIG`` and
        if you run any database command like ``hckr db query <QUERY>`` without providing configuration using
        ``-c/--config`` flag this config will be used.

    **Command Reference**:
    """

    set_default_config(service, config_name, config_path)


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
@config_file_path_option
def configure_db(
    config_name,
    config_path,
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
    """
    This command configures database credentials based on the selected database type.

    .. hint::
       We currently support ``Postgres``, ``MySql``, ``Sqlite`` and  ``Snowflake``,
       Please feel free to raise an issue or Pull request if additional databases are needed.

    .. table:: Database Options mapping
       :widths: auto

       =====    =====
       1        Postgres
       2        Mysql
       3        Sqlite
       4        Snowflake
       =====    =====

    **Example Usage**:

    * Setting up your database configuration using Prompt values


    .. code-block:: shell

        $ hckr configure db

    .. note::
       Using this cli will ask for information like database ``host``, ``port``, ``username`` etc. as per the database type selected.

    * Similarly, we can also provide all values using flag

    .. code-block:: shell

        $  hckr configure db --config-name test-config --database-type 3  --database-name mydb.sqlite

    .. note::
       here, we have configured ``Sqlite`` database with a name 'mydb.sqlite' by providing both flags in command line,
       for other database types, we will have to provide required flags accordingly.

    **Command Reference**:
    """

    set_config_value(config_name, config_path, CONFIG_TYPE, ConfigType.DATABASE)
    selected_db_type = db_type_mapping[database_type]
    set_config_value(config_name, config_path, DB_TYPE, selected_db_type)

    configure_creds(config_name, config_path, password, selected_db_type, user)

    if not database_name:
        database_name = click.prompt("Enter the database name")
    set_config_value(config_name, config_path, DB_NAME, database_name)

    configure_host(
        config_name,
        config_path,
        account,
        host,
        port,
        role,
        schema,
        selected_db_type,
        warehouse,
    )

    PSuccess(
        f"Database configuration saved successfully in config instance '{config_name}'"
    )
    list_config(config_path, config_name)
