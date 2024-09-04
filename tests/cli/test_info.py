import os

from click.testing import CliRunner

from hckr.cli.info import python, java, disk, shell


def test_info_java():
    runner = CliRunner()
    result = runner.invoke(java)
    print(result.output)
    assert result.exit_code == 0
    assert f"Java Version:" in result.output


def test_info_python():
    runner = CliRunner()
    result = runner.invoke(python)
    print(result.output)
    assert result.exit_code == 0
    assert f"Python Version:" in result.output


# TODO: failing in gh-actions
def test_info_shell():
    runner = CliRunner()
    result = runner.invoke(shell)
    os.environ["SHELL"] = "/bin/bash" # setting as in Github Actions, this is coming as '' even though $SHELL is present
    print(result.output)
    assert result.exit_code == 0
    assert f"Current shell:" in result.output


def test_info_disk():
    runner = CliRunner()
    result = runner.invoke(disk)
    print(result.output)
    assert result.exit_code == 0
    assert f"Disk Space" in result.output
