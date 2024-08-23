# from ..utils.MessageUtils import *
import logging

import click
import rich
from cron_descriptor import get_description  # type: ignore
from rich.panel import Panel

from ..utils.ConfigUtils import load_config, config_path, ensure_config_file, DEFAULT_CONFIG, configMessage, \
    list_config, set_config_value, get_config_value


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
    set_config_value(config, key, value)
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


@configure.command()
@common_config_options
@click.option(
    "-a",
    "--all",
    default=False,
    is_flag=True,
    help="Whether to show all configs (default: False)"
)
def show(config, all):
    """List configuration values."""
    list_config(config, all)


@configure.command('db')
@click.option('--host', prompt=True, help='Database host')
@click.option('--port', prompt=True, help='Database port')
@click.option('--user', prompt=True, help='Database user')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Database password')
@click.option('--dbname', prompt=True, help='Database name')
@click.pass_context
def configure_db(ctx, host, port, user, password, dbname):
    """Configure database credentials."""
    set_config_value('database', 'host', host)
    set_config_value('database', 'port', port)
    set_config_value('database', 'user', user)
    set_config_value('database', 'password', password)
    set_config_value('database', 'dbname', dbname)
    click.echo("Database configuration saved successfully.")
