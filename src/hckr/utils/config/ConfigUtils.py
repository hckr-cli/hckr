import configparser
import logging

import rich
from rich.panel import Panel

from .. import MessageUtils
from ..MessageUtils import PWarn, PSuccess, PInfo, PError
from ...__about__ import __version__
from .Constants import config_path, DBType, DEFAULT_CONFIG

# Define the default configuration file path, this can't be changed, although user can have multile instances using
# --config


def load_config():
    """Load the INI configuration file."""
    config = configparser.ConfigParser()
    if not config_exists():
        PWarn(
            f"Config file [magenta]{config_path}[/magenta] doesn't exists or empty,"
            f" Please run init command to create one \n "
            "[bold green]hckr config init"
        )
        exit(1)
    config.read(config_path)
    return config


def config_exists() -> bool:
    """
    Check if config file exists and is not empty.

    :return: True if config file exists and is not empty, False otherwise.
    :rtype: bool
    """
    if not config_path.exists():
        return False
    if config_path.stat().st_size == 0:
        return False
    with config_path.open("r") as file:
        content = file.read().strip()
        if not content:
            return False
    return True


def init_config(overwrite):
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.touch(exist_ok=True)
        default_config = {
            DEFAULT_CONFIG: {
                "version": f"{__version__}",
                "config_type": "default",
            },
            "CUSTOM": {
                "key": f"value",
            },
        }
        config = configparser.ConfigParser()
        config.read_dict(default_config)
        with config_path.open("w") as config_file:
            config.write(config_file)
        PSuccess(f"Config file created at {config_path}")
    elif overwrite:
        PInfo(
            f"Config file already exists at {config_path}, [magenta]-o/--overwrite[/magenta] passed \n"
            "[yellow]Deleting existing file"
        )
        config_path.unlink()
        init_config(overwrite=False)
    else:
        PWarn(
            f"Config file already exists at [yellow]{config_path}[/yellow],"
            " please pass [magenta]-o/--overwrite[/magenta] to recreate"
        )


def set_config_value(section, key, value, override=False):
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
        PInfo(f"Config \[{section}] doesn't exist, Adding")
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
