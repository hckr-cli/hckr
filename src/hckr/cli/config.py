import click

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
    This command adds a new entry to the config file with key and value

    **Example Usage**:

    * Setting a value inside DEFAULT config

    .. code-block:: shell

        $ hckr config set database_host 127.0.0.1

    * Similarly, we can also set a value in specific configuration, configuration will be created if not exists

    .. code-block:: shell

        $ hckr config set database_host 127.0.0.1 --config MY_DATABASE

    **Command Reference**:
    """

    configMessage(config)
    set_config_value(config, key, value)
    PSuccess(f"[{config}] {key} <- {value}")


@config.command()
@common_config_options
@click.argument("key")
def get(config, key):
    """
    This command returns value for a key in a configuration

    **Example Usage**:

    * Getting a value for key in DEFAULT config

    Note - DEFAULT config is parent of all other configurations and others will inherit its values if not overridden

    .. code-block:: shell

        $ hckr config get database_host

    * Similarly, we can also get a value in specific configuration

    .. code-block:: shell

        $ hckr config get database_host --config MY_DATABASE

    **Command Reference**:
    """

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
    help="Whether to shows a list of all configs (default: False)",
)
def list(config, all):
    """
    This command show list of all keys available in given configuration,
    we can also see values in all configurations by providing -a/--all flag

    **Example Usage**:

    * Getting values for keys in DEFAULT config

    Note - DEFAULT config is parent of all other configurations and others will inherit its values if not overridden

    .. code-block:: shell

        $ hckr config list

    * Similarly, we can also get all values in a specific configuration using -c/--config flag

    .. code-block:: shell

        $ hckr config list -c MY_DATABASE

    * Additionally, we can also see all configurations using -a/--all flag

    .. code-block:: shell

        $ hckr config list --all

    **Command Reference**:
    """
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
     This command Initializes the configuration for the application,
    we can also use this option to overwrite existing config and reinitialize.

    **Example Usage**:

    * Initialising config file .hckrcfg with default settings

    .. code-block:: shell

        $ hckr config init

    * Similarly, we can also delete existing file and recreate using -o/--overwrite flag

    .. code-block:: shell

        $ hckr config init --overwrite

    **Command Reference**:
    """
    init_config(overwrite)
