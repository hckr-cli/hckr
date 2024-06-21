import click


@click.group(
    help="crypto commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def crypto():
    pass
