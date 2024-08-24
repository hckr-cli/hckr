import logging
from configparser import NoSectionError, NoOptionError

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import click

from hckr.utils import ConfigUtils
from hckr.utils.ConfigUtils import ConfigType, DBType, load_config
from hckr.utils.MessageUtils import PError


def get_db_url(section):
    """
    This function retrieves a database URL based on the given configuration section.
    :param section: The name of the configuration section to retrieve the database URL from.
    :return: The database URL.
    """
    config = ConfigUtils.load_config()
    try:
        config_type = config.get(section, "config_type")
        if config_type != ConfigType.DATABASE:
            PError(f"The configuration {section} is not database type\n"
                   " Please use [magenta]hckr configure db[/magenta] to configure database.")
            exit(1)
        db_type = config.get(section, "database_type")

        if db_type == DBType.SQLite:
            dbname = config.get(section, "dbname")
            return f"sqlite:///{dbname}"

        elif db_type in [DBType.PostgreSQL, DBType.MySQL]:
            return _get_jdbc_url(config, section, db_type)

        elif db_type == DBType.Snowflake:
            return _get_snowflake_url(config, section)

    except NoOptionError as e:
        PError(f"Config {section} is not configured correctly\n {e}")
        exit(1)


def _get_jdbc_url(config, section, db_type):
    user = config.get(section, "user")
    password = config.get(section, "password")
    host = config.get(section, "host")
    port = config.get(section, "port")
    dbname = config.get(section, "dbname")
    if db_type == DBType.PostgreSQL:
        return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    elif db_type == DBType.MySQL:
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
    else:
        logging.debug(f"Invalid db_type: {db_type} in get_jdbc_url()")
        PError("Error occured while creating JDBC Url")
        exit(1)


def _get_snowflake_url(config, section):
    user = config.get(section, "user")
    password = config.get(section, "password")
    account = config.get(section, "account")
    warehouse = config.get(section, "warehouse")
    role = config.get(section, "role")
    dbname = config.get(section, "dbname")
    schema = config.get(section, 'schema')
    return (
        f"snowflake://{user}:{password}@{account}/{dbname}/{schema}"
        f"?warehouse={warehouse}&role={role}"
    )
