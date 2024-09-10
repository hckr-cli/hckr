import click

from ..utils.MessageUtils import PError, PSuccess
from ..utils.config.ConfigUtils import (
    init_config,
    configMessage,
    list_config,
    set_config_value,
    get_config_value,
    common_config_options,
    config_file_path_option,
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


@config.command()
@common_config_options
@click.argument("key")
@click.argument("value")
def set(config, config_path, key, value):
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
    set_config_value(config, config_path, key, value)
    PSuccess(f"[{config}] {key} <- {value}")


@config.command()
@common_config_options
@click.argument("key")
def get(config, config_path, key):
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
        value = get_config_value(config, config_path, key)
        PSuccess(f"[{config}] {key} = {value}")
    except ValueError as e:
        PError(f"{e}")


@config.command("list")
@config_file_path_option
def list_configs(config_path):
    """
    This command show list all configurations and their key values

    **Example Usage**:

    * We can also see all configuration list command

    .. code-block:: shell

        $ hckr config list

    **Command Reference**:
    """
    list_config(config_path, _all=True)


@config.command()
@common_config_options
def show(config, config_path):
    """
    This command show list of all keys available in the given configuration,

    **Example Usage**:

    * Getting values for keys in DEFAULT config

    Note - DEFAULT config is parent of all other configurations and others will inherit its values if not overridden

    .. code-block:: shell

        $ hckr config show

    * Similarly, we can also get all values in a specific configuration using -c/--config flag

    .. code-block:: shell

        $ hckr config show -c MY_DATABASE

    **Command Reference**:
    """
    list_config(
        config_path,
        config,
    )


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
