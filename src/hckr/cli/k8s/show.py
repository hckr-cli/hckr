from time import sleep

from ..k8s import k8s
from ...utils.CronUtils import run_progress_barV2, run_progress_bar

from ...utils.K8sUtils import list_namespaces, list_pods
from ...utils.MessageUtils import info, colored
import click


@k8s.group(
    help="List Kubernetes resources",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def show():
    pass


@show.command()
def namespaces():
    """
    This Lists all namespaces

    **Example Usage**:

    .. code-block:: shell

        $ hckr k8s show ns

    **Command Reference**:
    """

    info("Listing all namespaces")
    list_namespaces()


@show.command()
@click.option("-n", "--namespace", default="default", help="Kubernetes namespace")
@click.option(
    "-w",
    "--watch",
    help="This will enable continuous running of this command, every given of seconds",
)
@click.option(
    "-c",
    "--count",
    default=10,
    help="Number of Pods to show",
    required=False,
)
def pods(namespace, count, watch):
    """
    This Lists all Pods in a given namespace

    **Example Usage**:

    .. code-block:: shell

        $ hckr k8s show ns

    **Command Reference**:
    """
    info(f"Listing all Pods in namespace: {namespace}")
    if watch:
        info(f"Watch {colored('enabled', 'yellow')}, running this command every {watch} seconds")
        while True:
            list_pods(namespace, count)
            run_progress_barV2(int(watch))

    else:
        list_pods(namespace, count)
