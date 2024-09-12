import configparser
import logging
from pathlib import Path

import click

from .Constants import DEFAULT_CONFIG, DEFAULT_CONFIG_PATH
from .. import MessageUtils
from ..MessageUtils import PWarn, PSuccess, PInfo, PError


def config_file_path_option(func):
    func = click.option(
        "-f",
        "--config-path",
        help=f"Config file path, default: ``~/.hckrcfg``",
        default=DEFAULT_CONFIG_PATH,
    )(func)
    return func


def common_config_options(func):
    func = click.option(
        "-c",
        "--config",
        help=f"Config instance, default: ``{DEFAULT_CONFIG}``",
        default=DEFAULT_CONFIG,
    )(func)
    return config_file_path_option(func)


def load_config(config_path: str):
    """Load the INI configuration file."""
    logging.debug(f"Loading config from {config_path}")
    config = configparser.ConfigParser()
    if not config_exists(config_path):
        PError(
            f"Config file [magenta]{config_path}[/magenta] doesn't exists or empty,"
            f" Please run init command to create one \n "
            "[bold green]hckr config init"
        )
    config.read(config_path)
    return config


def config_exists(config_path) -> bool:
    """
    Check if config file exists and is not empty.
    """
    _config_path = Path(config_path)
    if not _config_path.exists():
        return False
    if _config_path.stat().st_size == 0:
        return False
    with _config_path.open("r") as file:
        content = file.read().strip()
        if not content:
            return False
    return True


def init_config(config_path, overwrite):
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.touch(exist_ok=True)
        default_config = {
            DEFAULT_CONFIG: {
                "config_type": "default",
            },
            "CUSTOM": {
                "key": "value",
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
        init_config(config_path, overwrite=False)
    else:
        PWarn(
            f"Config file already exists at [yellow]{config_path}[/yellow],"
            " please pass [magenta]-o/--overwrite[/magenta] to recreate"
        )


def set_config_value(section, config_path, key, value):
    """
    Sets a configuration value in a configuration file.
    """
    logging.debug(f"Setting [{section}] {key} = {value}")
    config = load_config(config_path)
    if not config.has_section(section) and section != DEFAULT_CONFIG:
        PInfo(f"Config [yellow]\[{section}][/yellow] doesn't exist, Adding a new one")
        config.add_section(section)
    config.set(section, key, value)
    with Path(config_path).open("w") as config_file:
        config.write(config_file)


def set_default_config(service, config_name, config_path):
    config = load_config(config_path=config_path)
    if config.has_section(config_name):
        if get_config_value(config_name, config_path, "config_type") == service:
            set_config_value(DEFAULT_CONFIG, config_path, service, config_name)
            PSuccess(
                f"[{DEFAULT_CONFIG}] [yellow]{service} = {config_name}",
                title="[green]Default config for "
                f"[magenta]{service}[/magenta] configured",
            )
        else:
            PError(
                f"Config [red]\[{config_name}][/red] is not of config type [yellow]{service}"
            )
    else:
        PError(f"Config [red]\[{config_name}][/red] doesn't exists.")


def get_config_value(section, config_path, key) -> str:
    logging.debug(f"Getting [{section}] {key} ")
    config = load_config(config_path)
    if section != DEFAULT_CONFIG and not config.has_section(section):
        PError(f"config '{section}' not found in the configuration.")
        # raise ValueError(f"Section '{section}' not found in the configuration.")
    if not config.has_option(section, key):
        PError(f"Key '{key}' not found in config '{section}'.")
        # raise ValueError(f"Key '{key}' not found in section '{section}'.")
    return config.get(section, key)


def _list_config_util(config, section):
    if section == DEFAULT_CONFIG:
        PSuccess(
            (
                "\n".join(
                    [f"{key} = {value}" for key, value in config.items("DEFAULT")]
                )
                if config.items(section)
                else "NOTHING FOUND"
            ),
            title=f"[green]\[DEFAULT]",
        )
    elif config.has_section(section):
        PSuccess(
            (
                "\n".join([f"{key} = {value}" for key, value in config.items(section)])
                if config.items(section)
                else "NOTHING FOUND"
            ),
            title=f"[green]\[{section}]",
        )
    else:
        PError(
            f"Config [yellow]\[{section}][/yellow] not found\nAvailable configs: [yellow]{config.sections()}"
        )


def list_config(config_path, section=DEFAULT_CONFIG, _all=False):
    config = load_config(config_path)
    if _all:
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
