from click.testing import CliRunner

from hckr.cli.cron import *


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


def test_cron_run_invalid_cmd():
    runner = CliRunner()
    expr = "*/1 * * * *"  # invalid command
    cmd = "lsdf -la"
    result = runner.invoke(run, ["--seconds", "5", "--cmd", cmd])
    assert (
        "Error in command execution /bin/sh: lsdf: command not found" in result.output
    )


def test_cron_run_no_schedule():
    runner = CliRunner()
    cmd = "echo 'hello world!'"
    result = runner.invoke(run, ["--cmd", cmd])
    print(result.output)
    assert "Please provide either --expr or --seconds to pass schedule" in result.output


def test_cron_run_both_schedule():
    runner = CliRunner()
    cmd = "echo 'hello world!'"
    expr = "* 2 3 * *"

    result = runner.invoke(run, ["--cmd", cmd, "--expr", expr, "--seconds", "10"])
    print(result.output)
    assert (
        "Please use either --expr or --seconds to pass schedule, can't use both"
        in result.output
    )


def test_test():
    from rich.console import Console
    from rich.box import Box
    from rich import box
    from rich.text import Text

    def print_in_rich_box(text, style="bold blue"):
        console = Console()
        # Create a Text instance with the desired style
        text = Text(text, style=style)
        # Print the text in a box
        console.print(text)

    # Example usage
    print_in_rich_box("Hello, World!\nThis is text inside a rich box.")
