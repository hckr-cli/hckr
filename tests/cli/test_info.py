from click.testing import CliRunner

from hckr.cli.info import hello, version
from hckr.__about__ import __version__


def test_info_hello_world():
    runner = CliRunner()
    name = "ashish"
    result = runner.invoke(hello)
    print(result.output)
    assert f"Hello World" in result.output


def test_info_hello_name():
    runner = CliRunner()
    name = "ashish"
    result = runner.invoke(hello, ["--name", name])
    print(result.output)
    assert f"Hello {name}" in result.output


def test_info_version():
    runner = CliRunner()
    result = runner.invoke(version)
    print(result.output)
    assert f"Version: devd=={__version__}" in result.output
