from ..k8s import k8s

from ...utils.K8sUtils import list_namespaces, list_pods
from ...utils.MessageUtils import info
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
def pods(namespace):
    """
    This Lists all Pods in a given namespace

    **Example Usage**:

    .. code-block:: shell

        $ hckr k8s show ns

    **Command Reference**:
    """

    info(f"Listing all Pods in namespace :{namespace}")
    list_pods(namespace)
