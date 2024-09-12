import random
import string

from hckr.cli.config import set, get, list_configs, show
from tests.testUtils import _get_args_with_config_path


def _get_random_string(length):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


# CONFIG GET AND SET
def test_config_get_set_default(cli_runner):
    _key = f"key_{_get_random_string(5)}"
    _value = f"value_{_get_random_string(5)}"
    result = cli_runner.invoke(set, _get_args_with_config_path([_key, _value]))
    assert result.exit_code == 0
    assert f"[DEFAULT] {_key} <- {_value}" in result.output

    # testing get
    result = cli_runner.invoke(get, _get_args_with_config_path([_key]))
    assert result.exit_code == 0
    assert f"[DEFAULT] {_key} = {_value}" in result.output


def test_config_get_set_custom_config(cli_runner):
    _key = f"key_{_get_random_string(5)}"
    _value = f"value_{_get_random_string(5)}"
    _CONFIG = "CUSTOM"
    result = cli_runner.invoke(
        set, _get_args_with_config_path(["--config", _CONFIG, _key, _value])
    )
    assert result.exit_code == 0
    assert f"[{_CONFIG}] {_key} <- {_value}" in result.output

    # testing get
    result = cli_runner.invoke(
        get, _get_args_with_config_path(["--config", _CONFIG, _key])
    )
    assert result.exit_code == 0
    assert f"[{_CONFIG}] {_key} = {_value}" in result.output


def test_config_show(cli_runner):
    result = cli_runner.invoke(show, _get_args_with_config_path([]))
    assert result.exit_code == 0
    assert "[DEFAULT]" in result.output


def test_config_show_custom(cli_runner):
    _CONFIG = "CUSTOM"
    result = cli_runner.invoke(show, _get_args_with_config_path(["--config", _CONFIG]))
    assert result.exit_code == 0
    assert "[CUSTOM]" in result.output


def test_config_list(cli_runner):
    result = cli_runner.invoke(list_configs, _get_args_with_config_path([]))
    assert "[DEFAULT]" in result.output
    assert "[CUSTOM]" in result.output


# NEGATIVE USE CASES
def test_config_get_set_missing_key(cli_runner):
    result = cli_runner.invoke(set, _get_args_with_config_path([]))
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing argument 'KEY'" in result.output


def test_config_set_missing_value(cli_runner):
    result = cli_runner.invoke(set, _get_args_with_config_path(["key"]))
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing argument 'VALUE'" in result.output
