import click


@click.group(
    help="Kubernetes commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def k8s():
    pass
