from click.testing import CliRunner

from hckr.cli.dt import now, convert_time


def test_dt_now():
    runner = CliRunner()
    result = runner.invoke(now, ["--timezone", "UTC"])
    assert result.exit_code == 0
    assert "Current time in UTC" in result.output


def test_dt_convert():
    runner = CliRunner()
    result = runner.invoke(
        convert_time,
        [
            "--datetime",
            "2024-01-01 10:00:00",
            "--from-tz",
            "UTC",
            "--to-tz",
            "US/Pacific",
        ],
    )
    assert result.exit_code == 0
    assert "US/Pacific" in result.output
