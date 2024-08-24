import configparser
import logging
from enum import Enum
from pathlib import Path
from readline import set_completer

import click
import rich
from rich.panel import Panel

from . import MessageUtils
from ..__about__ import __version__

# Define the default configuration file path, this can't be changed, although user can have multile instances using --config
config_path = Path.home() / ".hckrcfg"
DEFAULT_CONFIG = "DEFAULT"


class DBType(str, Enum):
    PostgreSQL = ("PostgreSQL",)
    MySQL = ("MySQL",)
    SQLite = ("SQLite",)
    Snowflake = ("Snowflake",)

    def __str__(self):
        return self.value


db_type_mapping = {
    "1": DBType.PostgreSQL,
    "2": DBType.MySQL,
    "3": DBType.SQLite,
    "4": DBType.Snowflake,
}


def load_config():
    """Load the INI configuration file."""
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def check_config() -> bool:
    return config_path.exists()


def init_config():
    """
    Ensures the existence of a configuration file at the specified path.

    :param config_path: The path to the configuration file.
    :return: None

    This function creates a configuration file at the specified path if it does not already exist. It also creates any necessary parent directories. The configuration file is empty initially, but a default configuration is written to it using configparser. The default configuration includes a 'DEFAULT' section with a 'version' option that contains the value of the __version__ global variable.

    Example Usage:
    --------------
    ensure_config_file(Path('/path/to/config.ini'))
    """
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.touch(exist_ok=True)
        default_config = {
            DEFAULT_CONFIG: {
                "version": f"{__version__}",
            },
            "CUSTOM": {
                "key": f"value",
            },
        }
        config = configparser.ConfigParser()
        config.read_dict(default_config)
        with config_path.open("w") as config_file:
            config.write(config_file)
        MessageUtils.info(f"Creating default config file {config_path}")
    else:
        logging.debug(f"Config file {config_path} already exists ")


def set_config_value(section, key, value):
    """
    Sets a configuration value in a configuration file.

    :param section: The name of the configuration section.
    :param key: The key of the configuration value.
    :param value: The value to set.
    :return: None

    This function sets a configuration value in a configuration file. It first logs the action using the `logging.debug()` function. Then, it loads the configuration file using the `load_config()` function. If the configuration file does not have the specified section and the section is not the default section, it adds the section to the configuration file. Next, it sets the value for the key in the specified section. Finally, it writes the updated configuration file to disk.

    After setting the configuration value, the function displays an information message using the `MessageUtils.info()` function.

    Note: This function assumes that the `logging` and `MessageUtils` modules are imported and configured properly.

    Example Usage:
    set_config_value("database", "username", "admin")
    """
    logging.debug(f"Setting [{section}] {key} = {value}")
    config = load_config()
    if not config.has_section(section) and section != DEFAULT_CONFIG:
        logging.debug(f"Adding section {section}")
        config.add_section(section)
    config.set(section, key, value)
    with config_path.open("w") as config_file:
        config.write(config_file)


def get_config_value(section, key) -> str:
    """
    :param section: The section of the configuration file where the desired value is located.
    :param key: The key of the value within the specified section.
    :return: The value corresponding to the specified key within the specified section of the configuration file.

    """
    logging.debug(f"Getting [{section}] {key} ")
    config = load_config()
    if section != DEFAULT_CONFIG and not config.has_section(section):
        raise ValueError(f"Section '{section}' not found in the configuration.")
    if not config.has_option(section, key):
        raise ValueError(f"Key '{key}' not found in section '{section}'.")
    return config.get(section, key)


def show_config(config, section):
    if section == DEFAULT_CONFIG:
        rich.print(
            Panel(
                (
                    "\n".join(
                        [f"{key} = {value}" for key, value in config.items("DEFAULT")]
                    )
                    if config.items("DEFAULT")
                    else "NOTHING FOUND"
                ),
                expand=True,
                title=f"\[DEFAULT]",
            )
        )
    elif config.has_section(section):
        rich.print(
            Panel(
                (
                    "\n".join(
                        [f"{key} = {value}" for key, value in config.items(section)]
                    )
                    if config.items(section)
                    else "NOTHING FOUND"
                ),
                expand=True,
                title=f"\[{section}]",
            )
        )
    else:
        rich.print(
            Panel(
                f"config {section} not found",
                expand=True,
                title="Error",
            )
        )


def list_config(section, all=False):
    """
    List Config

    This function takes a section parameter and lists the configuration values for that section from the loaded configuration file. If the section is found in the configuration file, it will print the section name and all key-value pairs associated with that section. If the section is not found, it will display an error message.

    :param section: The section name for which the configuration values should be listed.
    :return: None
    """
    config = load_config()
    if all:
        MessageUtils.info("Listing all config")
        show_config(config, DEFAULT_CONFIG)
        for section in config.sections():
            show_config(config, section)
    else:
        configMessage(section)
        show_config(config, section)


def configMessage(config):
    if config == DEFAULT_CONFIG:
        MessageUtils.info(f"Using default config: [magenta]{DEFAULT_CONFIG}")
    else:
        MessageUtils.info(f"Using config: [magenta]{config}")


# Function to retrieve database credentials
def get_db_creds(section):
    config = load_config()
    try:
        host = config.get(section, "host")
        port = config.get(section, "port")
        user = config.get(section, "user")
        password = config.get(section, "password")
        dbname = config.get(section, "dbname")
        return {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "dbname": dbname,
        }
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        click.echo(f"Error: {e}", err=True)
        return None
