import click

from .ConfigUtils import set_config_value
from .Constants import (
    DBType,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_ACCOUNT,
    DB_WAREHOUSE,
    DB_ROLE,
    DB_SCHEMA,
)


def configure_host(
    account, config_name, host, port, role, schema, selected_db_type, warehouse
):
    if selected_db_type in [DBType.PostgreSQL, DBType.MySQL]:
        if not host:
            host = click.prompt("Enter the database host (e.g., localhost, 127.0.0.1)")
        if not port:
            port = click.prompt("Enter the database port (e.g., 5432 for PostgreSQL)")

        set_config_value(config_name, DB_HOST, host)
        set_config_value(config_name, DB_PORT, port)

    elif selected_db_type == DBType.Snowflake:
        if not account:
            account = click.prompt("Enter the Snowflake Account Id")
        if not schema:
            schema = click.prompt("Enter the Snowflake schema name")
        if not warehouse:
            warehouse = click.prompt("Enter the Snowflake warehouse name")
        if not role:
            role = click.prompt("Enter the Snowflake role")
        set_config_value(config_name, DB_ACCOUNT, account)
        set_config_value(config_name, DB_WAREHOUSE, warehouse)
        set_config_value(config_name, DB_SCHEMA, schema)
        set_config_value(config_name, DB_ROLE, role)


def configure_creds(config_name, password, selected_db_type, user):
    if selected_db_type != DBType.SQLite:
        if not user:
            user = click.prompt("Enter the database user (e.g., root)")
        if not password:
            password = click.prompt(
                "Enter the database password (input hidden)",
                hide_input=True,
                confirmation_prompt=True,
            )
        # common values
        set_config_value(config_name, DB_USER, user)
        set_config_value(config_name, DB_PASSWORD, password)
