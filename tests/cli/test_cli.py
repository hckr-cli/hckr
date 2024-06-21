from click.testing import CliRunner

from hckr.cli import cli
from hckr.__about__ import __version__


def test_hckr():
    runner = CliRunner()
    result = runner.invoke(cli)
    print(result.output)
    assert result.exit_code == 0
    assert __version__ in result.output
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert (
        """Options:
  -v, --verbose  Enable verbose output, use -v for INFO and -vv for DEBUG
  --version      Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  cron    cron commands
  crypto  crypto commands
  hash    hash commands
  info    info commands"""
        in result.output
    )
