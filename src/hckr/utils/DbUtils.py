import logging
from configparser import NoOptionError

import click
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from hckr.utils import MessageUtils
from hckr.utils.DataUtils import print_df_as_table
from hckr.utils.MessageUtils import PError, PInfo
from hckr.utils.config import ConfigUtils
from hckr.utils.config.ConfigUtils import list_config, load_config
from hckr.utils.config.Constants import (
    ConfigType,
    DBType,
    DB_NAME,
    DB_USER,
    CONFIG_TYPE,
    DB_TYPE,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_ACCOUNT,
    DB_WAREHOUSE,
    DB_ROLE,
    DB_SCHEMA,
    DEFAULT_CONFIG,
)


def get_db_url(section, config_path):
    """
    This function retrieves a database URL based on the given configuration section.
    :param section: The name of the configuration section to retrieve the database URL from.
    :return: The database URL.
    """
    # Load the default config file to get the default section if none is provided
    if section == DEFAULT_CONFIG:
        MessageUtils.info(
            "No config is provided, trying to fetch [yellow]default database config[/yellow]"
            " from [magenta]\[DEFAULT][/magenta] config"
        )
        config = load_config(config_path)
        if not config.has_option(DEFAULT_CONFIG, str(ConfigType.DATABASE)):
            list_config(config_path, DEFAULT_CONFIG)
            PError(
                f"No configuration provided, and no default is set inside [yellow]{DEFAULT_CONFIG}[/yellow] config"
                "\nPlease provide a configuration using [yellow]-c/--config[/yellow] "
                "or configure a default using [magenta]hckr configure set-default db"
            )
        else:
            MessageUtils.info(
                f"No configuration section provided, Using default set [yellow]{section}"
            )
        section = ConfigUtils.get_config_value(
            DEFAULT_CONFIG, config_path, ConfigType.DATABASE
        )
        MessageUtils.info(
            f"Default database config [magenta]{section}[/magenta] inferred from"
            " [yellow]\[DEFAULT][/yellow] config"
        )

    config = ConfigUtils.load_config(config_path)
    if not config.has_section(section):
        PError(
            f"Config [yellow]{section}[/yellow] is not present in the config file [magenta]{config_path}"
        )

    try:
        config_type = config.get(section, CONFIG_TYPE)
        if config_type != ConfigType.DATABASE:
            PError(
                f"The configuration [yellow]{section}[/yellow] is not database type\n"
                " Please use [magenta]hckr configure db[/magenta] to configure database."
            )
        db_type = config.get(section, DB_TYPE)
        if db_type == DBType.SQLite:
            database_name = config.get(section, DB_NAME)
            return f"sqlite:///{database_name}"

        elif db_type in [DBType.PostgreSQL, DBType.MySQL]:
            return _get_jdbc_url(config, section, db_type)

        elif db_type == DBType.Snowflake:
            return _get_snowflake_url(config, section)

    except NoOptionError as e:
        PError(f"Config {section} is not configured correctly\n {e}")


def _get_jdbc_url(config, section, db_type):
    user = config.get(section, DB_USER)
    password = config.get(section, DB_PASSWORD)
    host = config.get(section, DB_HOST)
    port = config.get(section, DB_PORT)
    database_name = config.get(section, DB_NAME)
    if db_type == DBType.PostgreSQL:
        return f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
    elif db_type == DBType.MySQL:
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}"
    else:
        logging.debug(f"Invalid db_type: {db_type} in get_jdbc_url()")
        PError("Error occured while creating JDBC Url")


def _get_snowflake_url(config, section):
    user = config.get(section, DB_USER)
    password = config.get(section, DB_PASSWORD)
    account = config.get(section, DB_ACCOUNT)
    warehouse = config.get(section, DB_WAREHOUSE)
    role = config.get(section, DB_ROLE)
    database_name = config.get(section, DB_NAME)
    schema = config.get(section, DB_SCHEMA)
    return (
        f"snowflake://{user}:{password}@{account}/{database_name}/{schema}"
        f"?warehouse={warehouse}&role={role}"
    )


def execute_query(db_url, query, num_rows, num_cols):
    try:
        query = query.strip()
        engine = create_engine(db_url)
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
        click.echo("\n")
        PError(f"Error executing query: \n[red]{e}")
