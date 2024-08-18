import re
from click.testing import CliRunner

from hckr.cli.net import *


def test_net_speed():
    runner = CliRunner()
    result = runner.invoke(speed)
    print(result.output)
    assert (
            f"Servers" in result.output and
            "currently using" in result.output
    )
    assert (
            "Speed test results" in result.output and
            "Download Speed" in result.output and
            "Upload Speed" in result.output and
            "Ping" in result.output
    )
