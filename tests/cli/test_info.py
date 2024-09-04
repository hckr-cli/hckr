import os

from click.testing import CliRunner

from hckr.cli.info import python, java, disk, shell


def test_info_java():
    runner = CliRunner()
    result = runner.invoke(java)
    print(result.output)
    assert result.exit_code == 0
    assert "Java Version:" in result.output


def test_info_python():
    runner = CliRunner()
    result = runner.invoke(python)
    print(result.output)
    assert result.exit_code == 0
    assert "Python Version:" in result.output


# TODO: failing in gh-actions
def test_info_shell():
    runner = CliRunner()
    os.environ["SHELL"] = (
        "/bin/bash"  # setting as in GitHub Actions, this is coming as '' even though $SHELL is present
    )
    result = runner.invoke(shell)
    print(result.output)
    assert result.exit_code == 0
    assert "Current shell:" in result.output


def test_info_disk():
    runner = CliRunner()
    result = runner.invoke(disk)
    print(result.output)
    assert result.exit_code == 0
    assert "Disk Space" in result.output
