import click

from ..utils import MessageUtils
from ..utils.EnvUtils import list_env, set_env
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
    help="Environment variable commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def env():
    """
    Defines a command group for managing environment variables
    """
    pass



@env.command()
@click.argument('variable_name')
@click.argument('variable_value')
@click.option('--shell', type=click.Choice(['bash', 'zsh']), default='bash', help='Shell type')
def set(variable_name, variable_value, shell):
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
    set_env(variable_name, variable_value, shell)
    PSuccess(f"{variable_name} <- {variable_value}")


# @env.command()
# @click.argument("variable")
# def get(variable):
#     """
#     This command returns value for a env variable
#     **Example Usage**:
#
#     * Getting a value for key in DEFAULT config
#
#     Note - DEFAULT config is parent of all other configurations and others will inherit its values if not overridden
#
#     .. code-block:: shell
#
#         $ hckr config get database_host
#
#     * Similarly, we can also get a value in specific configuration
#
#     .. code-block:: shell
#
#         $ hckr config get database_host --config MY_DATABASE
#
#     **Command Reference**:
#     """
#
#     configMessage(config)
#     try:
#         value = get_config_value(config, key)
#         PSuccess(f"[{config}] {key} = {value}")
#     except ValueError as e:
#         PError(f"{e}")


@env.command("list")
@click.option('-p', '--pattern', required=False, default='.*')
@click.option('-i', '--ignore-case', is_flag=True, help='Ignore case distinctions.')
def env_list(pattern, ignore_case):
    """
    This command show list of all environment variables,

    **Example Usage**:

    * Getting values for keys in DEFAULT config

    Note - DEFAULT config is parent of all other configurations and others will inherit its values if not overridden

    .. code-block:: shell

        $ hckr env show

    * Similarly, we can also get all values in a specific configuration using -c/--config flag

    .. code-block:: shell

        $ hckr config show -c MY_DATABASE

    * Additionally, we can also see all configurations using -a/--all flag

    .. code-block:: shell

        $ hckr config show --all

    **Command Reference**:
    """
    MessageUtils.info("Listing all environment variables")
    list_env(pattern, ignore_case)
