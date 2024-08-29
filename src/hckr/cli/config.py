# from ..utils.MessageUtils import *

import click
import rich
from cron_descriptor import get_description  # type: ignore

from ..utils.MessageUtils import PError, PSuccess
from ..utils.config.ConfigUtils import (
    init_config,
    DEFAULT_CONFIG,
    configMessage,
    list_config,
    set_config_value,
    get_config_value,
)


@click.group(
    help="Config commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.pass_context
def config(ctx):
    """
    Defines a command group for managing application configurations. This group includes commands to set, get, show, and initialize configuration values.
    """
    pass


def common_config_options(func):
    func = click.option(
        "-c",
        "--config",
        help="Config instance, default: DEFAULT",
        default=DEFAULT_CONFIG,
    )(func)
    return func


@config.command()
@common_config_options
@click.argument("key")
@click.argument("value")
def set(config, key, value):
    """
    Sets a configuration value.

    Args:
        config (str): The configuration instance name. Default is defined by DEFAULT_CONFIG.
        key (str): The key of the config setting to change.
        value (str): The value to set for the specified key.

    Example:
        $ cli_tool configure set database_host 127.0.0.1
    """
    configMessage(config)
    set_config_value(config, key, value)
    PSuccess(f"[{config}] {key} <- {value}")


@config.command()
@common_config_options
@click.argument("key")
def get(config, key):
    """Get a configuration value."""
    configMessage(config)
    try:
        value = get_config_value(config, key)
        PSuccess(f"[{config}] {key} = {value}")
    except ValueError as e:
        PError(f"{e}")


@config.command()
@common_config_options
@click.option(
    "-a",
    "--all",
    default=False,
    is_flag=True,
    help="Whether to show all configs (default: False)",
)
def show(config, all):
    """List configuration values."""
    list_config(config, all)


@config.command()
@click.option(
    "-o",
    "--overwrite",
    default=False,
    is_flag=True,
    help="Whether to delete and recreate .hckrcfg file (default: False)",
)
def init(overwrite):
    """
    Initializes the configuration for the application.

    :return: None
    """
    init_config(overwrite)
