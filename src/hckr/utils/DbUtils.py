from configparser import NoSectionError, NoOptionError

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import click

from hckr.utils import ConfigUtils


def get_db_url(section):
    """
    This function retrieves a database URL based on the given configuration section.
    :param section: The name of the configuration section to retrieve the database URL from.
    :return: The database URL.
    """
    config = ConfigUtils.load_config()
    try:
        db_type = config.get(section, 'type')

        if db_type == 'sqlite':
            dbname = config.get(section, 'dbname')
            return f"sqlite:///{dbname}"

        elif db_type == 'postgresql':
            user = config.get(section, 'user')
            password = config.get(section, 'password')
            host = config.get(section, 'host')
            port = config.get(section, 'port')
            dbname = config.get(section, 'dbname')
            return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

        elif db_type == 'mysql':
            user = config.get(section, 'user')
            password = config.get(section, 'password')
            host = config.get(section, 'host')
            port = config.get(section, 'port')
            dbname = config.get(section, 'dbname')
            return f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"

        elif db_type == 'snowflake':
            user = config.get(section, 'user')
            password = config.get(section, 'password')
            account = config.get(section, 'account')
            warehouse = config.get(section, 'warehouse')
            role = config.get(section, 'role')
            dbname = config.get(section, 'dbname')
            return (
                f"snowflake://{user}:{password}@{account}/{dbname}?"
                f"warehouse={warehouse}&role={role}"
            )

    except (NoSectionError, NoOptionError) as e:
        click.echo(f"Error: {e}", err=True)
        return None
