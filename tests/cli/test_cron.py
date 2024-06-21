import re
from click.testing import CliRunner

from hckr.cli.cron import *


# CRON DESC
def test_cron_desc():
    runner = CliRunner()
    expr = "* 2 3 * *"
    result = runner.invoke(desc, ["--expr", expr])
    # print(result.output)
    assert (
        f"Every minute, between 02:00 AM and 02:59 AM, on day 3 of the month"
        in result.output
    )


def test_cron_desc_invalid():
    runner = CliRunner()
    expr = "* a 3 * *"  # invalid command
    result = runner.invoke(desc, ["--expr", expr])
    # print(result.output)
    assert f"Invalid cron expression" in result.output


# CRON RUN POSITIVE


def test_cron_run_seconds():
    runner = CliRunner()
    expr = "*/1 * * * *"  # invalid command
    cmd = "echo 'hello world!'"
    result = runner.invoke(run, ["--seconds", "2", "--cmd", cmd, "--timeout", "3"])
    print(result.output)
    assert "Output [3/3]" in result.output
    assert "hello world!" in result.output
    assert "Running command: echo 'hello world!', Every 2 seconds" in result.output


def test_cron_run_expr():
    runner = CliRunner()
    expr = "*/1 * * * *"  # every minute
    cmd = "echo 'hello world!'"
    result = runner.invoke(run, ["--expr", expr, "--cmd", cmd, "--timeout", "1"])
    print(result.output)
    assert "Output [1/1]" in result.output
    assert "hello world!" in result.output
    assert "Running command: echo 'hello world!', Every minute" in result.output


# CRON RUN INVALID


def test_cron_run_invalid_cmd():
    runner = CliRunner()
    expr = "*/1 * * * *"  # invalid command
    cmd = "lsdf"
    pattern = re.compile(r"lsdf:.*not found")
    result = runner.invoke(run, ["--seconds", "5", "--cmd", cmd])
    assert "Error in command execution" in result.output
    # assert "not found" in result.output
    print(result.output)
    assert pattern.search(result.output), "Pattern not found"


def test_cron_run_invalid_expr():
    runner = CliRunner()
    expr = "*/1 * * * * *"  # invalid command
    cmd = "ls -la"
    result = runner.invoke(run, ["--expr", expr, "--cmd", cmd])
    assert "Invalid cron Expression: */1 * * * * *" in result.output
    assert "cron expression must have 5 places" in result.output


def test_cron_run_no_schedule():
    runner = CliRunner()
    cmd = "echo 'hello world!'"
    result = runner.invoke(run, ["--cmd", cmd])
    print(result.output)
    assert "Please provide either --seconds or --expr" in result.output


def test_cron_run_both_schedule():
    runner = CliRunner()
    cmd = "echo 'hello world!'"
    expr = "* 2 3 * *"

    result = runner.invoke(run, ["--cmd", cmd, "--expr", expr, "--seconds", "10"])
    print(result.output)
    assert result.exit_code != 0
    assert "Please use either --seconds or --expr, can't use both" in result.output
