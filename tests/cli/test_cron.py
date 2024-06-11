from click.testing import CliRunner

from hckr.cli.cron import desc


def test_cron_desc():
    runner = CliRunner()
    expr="* 2 3 * *"
    result = runner.invoke(desc, ["--expr", expr])
    # print(result.output)
    assert f"Every minute, between 02:00 AM and 02:59 AM, on day 3 of the month" in result.output


def test_cron_desc_invalid():
    runner = CliRunner()
    expr="* a 3 * *" # invalid command
    result = runner.invoke(desc, ["--expr", expr])
    # print(result.output)
    assert f"Invalid cron expression" in result.output
