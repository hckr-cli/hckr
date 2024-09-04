import os

from click.testing import CliRunner

from hckr.cli.env import get, set, env_list


def test_env_set():
    runner = CliRunner()
    os.environ["SHELL"] = (
        "/bin/bash"  # setting as in GitHub Actions, this is coming as '' even though $SHELL is present
    )
    result = runner.invoke(set, ["KEY1", "VALUE1"])
    print(result.output)
    assert result.exit_code == 0
    assert "Success: Value set and sourced in" in result.output
    assert "KEY1 <- VALUE1" in result.output


def test_env_get():
    runner = CliRunner()
    result = runner.invoke(get, "HOME")
    print(result.output)
    assert result.exit_code == 0
    assert "Success" in result.output
    assert "HOME =" in result.output


def test_env_list():
    runner = CliRunner()
    result = runner.invoke(env_list, [])
    print(result.output)
    assert result.exit_code == 0
    assert "Listing all environment variables" in result.output
    assert "HOME =" in result.output
