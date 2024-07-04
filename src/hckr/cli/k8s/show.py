from time import sleep

from ..k8s import k8s
from ...utils.CronUtils import run_progress_barV2, run_progress_bar

from ...utils.K8sUtils import list_namespaces, list_pods, list_contexts
from ...utils.MessageUtils import info, colored
import click


@k8s.group(
    help="List Kubernetes resources",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def show():
    pass


def common_k8s_options(func):
    func = click.option("-c", "--context", help="Kubernetes context to be used, [default: current context]")(
        func
    )
    return func


@common_k8s_options
@show.command()
def namespaces(context):
    """
    This Lists all namespaces

    **Example Usage**:

    .. code-block:: shell

        $ hckr k8s show namespaces

    **Command Reference**:
    """
    info(f"Using context: {context}")
    # info("Listing all namespaces")
    list_namespaces(context)


@show.command()
def contexts():
    """
    This Command Lists all contexts

    **Example Usage**:

    .. code-block:: shell

        $ hckr k8s show contexts

    **Command Reference**:
    """

    info("Listing all contexts")
    list_contexts()


@show.command()
@common_k8s_options
@click.option("-n", "--namespace", default="default", help="Kubernetes namespace")
@click.option(
    "--count",
    default=10,
    help="Number of Pods to show",
    required=False,
)
@click.option(
    "-w",
    "--watch",
    help="This will enable continuous running of this command, every given of seconds",
)
def pods(context, namespace, count, watch):
    """
    This Lists all Pods in a given namespace

    **Example Usage**:

    .. code-block:: shell

        $ hckr k8s show ns

    **Command Reference**:
    """
    info(f"Using context: {context}")
    info(f"Listing all Pods in namespace: {namespace}")
    if watch:
        info(f"Watch {colored('enabled', 'yellow')}, running this command every {watch} seconds")
        while True:
            list_pods(context, namespace, count)
            run_progress_barV2(int(watch))

    else:
        list_pods(context, namespace, count)
