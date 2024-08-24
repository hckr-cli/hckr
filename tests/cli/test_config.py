import random
import string

from click.testing import CliRunner

from hckr.cli.config import set, get, show


def _get_random_string(length):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


# CONFIG GET AND SET
def test_config_get_set_default():
    runner = CliRunner()
    _key = f"key_{_get_random_string(5)}"
    _value = f"value_{_get_random_string(5)}"
    result = runner.invoke(set, [_key, _value])
    assert result.exit_code == 0
    assert f"[DEFAULT] {_key} <- {_value}" in result.output

    # testing get
    result = runner.invoke(get, [_key])
    assert result.exit_code == 0
    assert f"[DEFAULT] {_key} = {_value}" in result.output


def test_config_get_set_custom_config():
    runner = CliRunner()
    _key = f"key_{_get_random_string(5)}"
    _value = f"value_{_get_random_string(5)}"
    _CONFIG = "CUSTOM"
    result = runner.invoke(set, ["--config", _CONFIG, _key, _value])
    assert result.exit_code == 0
    assert f"[{_CONFIG}] {_key} <- {_value}" in result.output

    # testing get
    result = runner.invoke(get, ["--config", _CONFIG, _key])
    assert result.exit_code == 0
    assert f"[{_CONFIG}] {_key} = {_value}" in result.output


def test_config_show():
    runner = CliRunner()
    _CONFIG = "CUSTOM"
    result = runner.invoke(show)
    assert result.exit_code == 0
    assert "[DEFAULT]" in result.output

    result = runner.invoke(show, ["--all"])
    assert "[DEFAULT]" in result.output
    assert "[CUSTOM]" in result.output


# NEGATIVE USE CASES
def test_config_get_set_missing_key():
    runner = CliRunner()
    result = runner.invoke(set, [])
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing argument 'KEY'" in result.output

    runner = CliRunner()
    result = runner.invoke(get, [])
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing argument 'KEY'" in result.output


def test_config_set_missing_value():
    runner = CliRunner()
    result = runner.invoke(set, ["key"])
    print(result.output)
    assert result.exit_code != 0
    assert "Error: Missing argument 'VALUE'" in result.output
