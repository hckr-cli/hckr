import click
import rich
import speedtest
from rich.panel import Panel
from yaspin import yaspin

from hckr.utils import NetUtils


@click.group(
    help="network commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def net():
    pass


def list_servers():
    st = speedtest.Speedtest()
    st.get_servers()  # Fetch the server list
    servers = st.servers
    for _, server_list in servers.items():
        for server in server_list:
            print(f"Server ID: {server['id']} - {server['sponsor']} in {server['name']}, {server['country']}")


# NOTE - keep command() empty to provide docstr
@net.command()
def speed():
    """
    find your internet speed.


    **Example Usage**:

    .. code-block:: shell

        $ hckr net speed


    **Command Reference**:
    """
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        servers, current_server = NetUtils.list_servers(st)
        servers_details = [
            (
                f"🔗[green]{server['id']} - {server['sponsor']}, {server['name']}[/green] <- [magenta]currently using[/magenta]"
                if server["id"] == current_server["id"]
                else f"🗄{server['id']} - {server['sponsor']}, {server['name']}"
            )
            for server in servers
        ]
        rich.print(
            Panel(
                "\n".join(servers_details) if servers_details else "NOTHING FOUND",
                expand=False,
                title="Servers",
            )
        )
        ping = st.results.ping
        with yaspin(
                text="Checking internet connection speeds...", color="green", timer=True
        ) as spinner:
            download_speed = st.download(threads=None) / 1_000_000  # Convert from bits/s to Mbps
            upload_speed = st.upload(threads=None) / 1_000_000  # Convert from bits/s to Mbps
            click.echo("\n")
            rich.print(
                Panel(
                    # [magenta]currently using[/magenta]
                    f"[blue]🛜 Ping:[/blue] [green]{ping:.2f} ms[/green]"
                    f"\n[yellow]⬇️ Download Speed:[/yellow] [green]{download_speed:.2f} Mbps[/green]"
                    f"\n[magenta]⬆️ Upload Speed:[/magenta] [green]{upload_speed:.2f} Mbps[/green]",
                    expand=False,
                    title="Speed test results",
                )
            )
            spinner.ok("✔")
    except speedtest.ConfigRetrievalError as e:
        click.echo(click.style(f"Failed to retrieve speedtest configuration. {e}", fg="red"))
    except speedtest.SpeedtestBestServerFailure as e:
        click.echo(click.style(f"Failed to find best server for speedtest. {e}", fg="red"))
    except speedtest.SpeedtestException as e:
        click.echo(click.style(f"A speedtest error occurred. {e}", fg="red"))
