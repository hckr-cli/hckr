# from ..utils.MessageUtils import *
import logging

import click
import rich
from cron_descriptor import get_description  # type: ignore
from rich.panel import Panel

from ..utils import MessageUtils
from ..utils.ConfigUtils import (
    load_config,
    config_path,
    ensure_config_file,
    DEFAULT_CONFIG,
    configMessage,
    list_config,
    set_config_value,
    get_config_value, db_type_mapping,
)


@click.group(
    help="Config commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.pass_context
def config(ctx):
    """
    Defines a command group for configuration-related commands.
    """
    ensure_config_file()


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
    rich.print(
        Panel(
            f"[{config}] {key} <- {value}",
            expand=True,
            title="Success",
        )
    )


@config.command()
@common_config_options
@click.argument("key")
def get(config, key):
    """Get a configuration value."""
    configMessage(config)
    try:
        value = get_config_value(config, key)
        rich.print(
            Panel(
                f"[{config}] {key} = {value}",
                expand=True,
                title="Success",
            )
        )
    except ValueError as e:
        rich.print(
            Panel(
                f"{e}",
                expand=True,
                title="Error",
            )
        )


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
