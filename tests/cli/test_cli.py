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


def test_test():
    import json
    from urllib.request import urlopen

    from rich.console import Console
    from rich.columns import Columns
    from rich.panel import Panel

    def get_content(user):
        """Extract text from user dict."""
        country = user["location"]["country"]
        name = f"{user['name']['first']} {user['name']['last']}"
        return f"[b]{name}[/b]\n[yellow]{country}"

    console = Console()
    import rich

    users = json.loads(urlopen("https://randomuser.me/api/?results=30").read())[
        "results"
    ]
    user_renderables = [Panel(get_content(user), expand=True) for user in users]
    rich.print()
    rich.print(Panel("Hello"))
