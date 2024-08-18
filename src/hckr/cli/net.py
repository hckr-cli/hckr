import click
import rich
import speedtest  # type: ignore
from rich.panel import Panel
from yaspin import yaspin  # type: ignore

from hckr.utils import NetUtils, MessageUtils
from hckr.utils.NetUtils import get_ip_addresses


@click.group(
    help="network commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def net():
    pass


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
                f"🌐 [green]{server['id']} - {server['sponsor']}, {server['name']}[/green] <- [magenta]currently using[/magenta]"
                if server["id"] == current_server["id"]
                else f"🌐 {server['id']} - {server['sponsor']}, {server['name']}"
            )
            for server in servers
        ]
        rich.print(
            Panel(
                "\n".join(servers_details) if servers_details else "NOTHING FOUND",
                expand=False,
                title="Speedtest.net Servers",
            )
        )
        ping = st.results.ping
        with yaspin(
            text="Checking internet connection speeds...", color="green", timer=True
        ) as spinner:
            download_speed = (
                st.download(threads=None) / 1_000_000
            )  # Convert from bits/s to Mbps
            upload_speed = (
                st.upload(threads=None) / 1_000_000
            )  # Convert from bits/s to Mbps
            click.echo("\n")
            rich.print(
                Panel(
                    # [magenta]currently using[/magenta]
                    f"[blue]⏱ Ping:[/blue] [green]{ping:.2f} ms[/green]"
                    f"\n[yellow]⬇ Download Speed:[/yellow] [green]{download_speed:.2f} Mbps[/green]"
                    f"\n[magenta]⬆ Upload Speed:[/magenta] [green]{upload_speed:.2f} Mbps[/green]",
                    expand=False,
                    title="Speed test results",
                )
            )
            spinner.ok("✔")
    except speedtest.ConfigRetrievalError as e:
        click.echo(
            click.style(f"Failed to retrieve speedtest configuration. {e}", fg="red")
        )
    except speedtest.SpeedtestBestServerFailure as e:
        click.echo(
            click.style(f"Failed to find best server for speedtest. {e}", fg="red")
        )
    except speedtest.SpeedtestException as e:
        click.echo(click.style(f"A speedtest error occurred. {e}", fg="red"))


@net.command()
@click.option(
    "-a",
    "--all",
    default=False,
    is_flag=True,
    help="Whether to show loopback addresses (default: False)",
)
def ips(all):
    """
    find your internet ip addresses.


    **Example Usage**:

    .. code-block:: shell

        $ hckr net ips

    **Command Reference**:
    """
    try:
        MessageUtils.success("Fetching IP addresses...")
        if all:
            MessageUtils.info(
                "-a/--all is passed listing down all IP addresses including loopback addresses"
            )
        ipV4s, ipV6s = get_ip_addresses(all)
        rich.print(
            Panel(
                "\n".join(ipV4s) if ipV4s else "No IpV4 Address FOUND",
                expand=True,
                title="IpV4 Addresses",
            )
        )
        rich.print(
            Panel(
                "\n".join(ipV6s) if ipV4s else "No IpV6 Address FOUND",
                expand=True,
                title="IpV6 Addresses",
            )
        )
    except Exception as e:
        MessageUtils.error(f"Some error occured while fetching IP addresses: {e}")
