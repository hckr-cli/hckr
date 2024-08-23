# from ..utils.MessageUtils import *
import logging

import click
import rich
from cron_descriptor import get_description  # type: ignore
from rich.panel import Panel

from ..utils import ConfigUtils, MessageUtils
from ..utils.ConfigUtils import load_config, config_path, ensure_config_file, DEFAULT_CONFIG, configMessage


@click.group(
    help="Config commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.pass_context
def configure(ctx):
    """
    Defines a command group for configuration-related commands.
    """
    ensure_config_file()


def common_config_options(func):
    func = click.option("-c", "--config", help="Config instance, default: DEFAULT", default=DEFAULT_CONFIG)(func)
    return func


@configure.command()
@common_config_options
@click.argument('key')
@click.argument('value')
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
    ConfigUtils.set_config_value(config, key, value)
    rich.print(
        Panel(
            f"[{config}] {key} <- {value}",
            expand=True,
            title="Success",
        )
    )

@configure.command()
@common_config_options
@click.argument('key')
def get(config, key):
    """Get a configuration value."""
    configMessage(config)
    try:
        value = ConfigUtils.get_config_value(config, key)
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


@configure.command()
@common_config_options
def show(config):
    """List configuration values."""
    configMessage(config)
    ConfigUtils.list_config(config)
