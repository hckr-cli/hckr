from click.testing import CliRunner

from hckr.cli import hello


def test_hello_world():
    runner = CliRunner()
    name = "ashish"
    result = runner.invoke(hello)
    print(result.output)
    assert f"Hello World" in result.output


def test_hello_name():
    runner = CliRunner()
    name = "ashish"
    result = runner.invoke(hello, ["--name", name])
    print(result.output)
    assert f"Hello {name}" in result.output
