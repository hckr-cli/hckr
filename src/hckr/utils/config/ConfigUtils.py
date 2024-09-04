import configparser
import logging

import rich
from rich.panel import Panel

from .Constants import config_path, DEFAULT_CONFIG
from .. import MessageUtils
from ..MessageUtils import PWarn, PSuccess, PInfo, PError
from ...__about__ import __version__


def load_config():
    """Load the INI configuration file."""
    config = configparser.ConfigParser()
    if not config_exists():
        PError(
            f"Config file [magenta]{config_path}[/magenta] doesn't exists or empty,"
            f" Please run init command to create one \n "
            "[bold green]hckr config init"
        )
    config.read(config_path)
    return config


def config_exists() -> bool:
    """
    Check if config file exists and is not empty.
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
    logging.debug(f"Getting [{section}] {key} ")
    config = load_config()
    if section != DEFAULT_CONFIG and not config.has_section(section):
        raise ValueError(f"Section '{section}' not found in the configuration.")
    if not config.has_option(section, key):
        raise ValueError(f"Key '{key}' not found in section '{section}'.")
    return config.get(section, key)


def _list_config_util(config, section):
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
                title="\[DEFAULT]",
            )
        )
    elif config.has_section(section):
        # TODO: replace these with PSuccess()
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
    config = load_config()
    if all:
        MessageUtils.info("Listing all config")
        _list_config_util(config, DEFAULT_CONFIG)
        for section in config.sections():
            _list_config_util(config, section)
    else:
        configMessage(section)
        _list_config_util(config, section)


def configMessage(config):
    if config == DEFAULT_CONFIG:
        MessageUtils.info(f"Using default config: [magenta]{DEFAULT_CONFIG}")
    else:
        MessageUtils.info(f"Using config: [magenta]{config}")
