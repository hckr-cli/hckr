from click.testing import CliRunner

from hckr.cli.info import hello, version
from hckr.__about__ import __version__


def test_info_hello_world():
    runner = CliRunner()
    result = runner.invoke(hello)
    assert result.exit_code == 0
    print(result.output)
    assert "Hello World" in result.output


def test_info_hello_name():
    runner = CliRunner()
    name = "ashish"
    result = runner.invoke(hello, ["--name", name])
    print(result.output)
    assert result.exit_code == 0
    assert f"Hello {name}" in result.output


def test_info_version():
    runner = CliRunner()
    result = runner.invoke(version)
    print(result.output)
    assert result.exit_code == 0
    assert f"Version: hckr=={__version__}" in result.output
