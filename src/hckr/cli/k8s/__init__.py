import click


def common_k8s_options(func):
    func = click.option(
        "-c",
        "--context",
        help="Kubernetes context to be used, [default: Current active context]",
    )(func)
    return func


@click.group(
    help="Kubernetes commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def k8s():
    pass
