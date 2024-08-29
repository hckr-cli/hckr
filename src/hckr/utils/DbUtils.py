import logging
from configparser import NoOptionError

from hckr.utils.MessageUtils import PError
from hckr.utils.config import ConfigUtils
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
)


def get_db_url(section):
    """
    This function retrieves a database URL based on the given configuration section.
    :param section: The name of the configuration section to retrieve the database URL from.
    :return: The database URL.
    """
    config = ConfigUtils.load_config()
    try:
        config_type = config.get(section, CONFIG_TYPE)
        if config_type != ConfigType.DATABASE:
            PError(
                f"The configuration {section} is not database type\n"
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
