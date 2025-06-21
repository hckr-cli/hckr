from click.testing import CliRunner
from hckr.cli.dt import dt, now, convert_time


def test_dt_now():
    runner = CliRunner()
    result = runner.invoke(now, ["--timezone", "UTC"])
    assert result.exit_code == 0
    assert "Current time in UTC" in result.output


def test_dt_convert():
    runner = CliRunner()
    result = runner.invoke(
        convert_time,


def test_dt_default():
    runner = CliRunner()
    result = runner.invoke(
        dt,
        ["--timezone", "UTC", "--format", "%Y-%m-%d %H:%M:%S", "2024-01-01T12:00:00"],
    )
    assert result.exit_code == 0
    assert "2024-01-01 12:00:00" in result.output


def test_dt_invalid_timezone():
    runner = CliRunner()
    result = runner.invoke(dt, ["--timezone", "Mars/Phobos"])
    assert result.exit_code != 0
    assert "Invalid timezone" in result.output
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
