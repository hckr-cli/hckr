from click.testing import CliRunner

from hckr.cli.net import speed, ips


def test_net_speed():
    runner = CliRunner()
    result = runner.invoke(speed)
    # print(result.output)
    assert "Servers" in result.output and "currently using" in result.output
    assert (
        "Speed test results" in result.output
        and "Download Speed" in result.output
        and "Upload Speed" in result.output
        and "Ping" in result.output
    )


def test_net_ips():
    runner = CliRunner()
    result = runner.invoke(ips)
    # print(result.output)
    assert (
        "Fetching IP addresses" in result.output
        and "IpV4 Addresses" in result.output
        and "IpV4 Addresses" in result.output
    )
