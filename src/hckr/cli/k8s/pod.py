from time import sleep

from ..k8s import k8s, common_k8s_options
from ...utils.CronUtils import run_progress_barV2, run_progress_bar

from ...utils.K8sUtils import list_namespaces, list_pods, list_contexts
from ...utils.MessageUtils import info, colored
import click


@k8s.group(
    help="Kubernetes pod related commands ",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def pod():
    pass


@pod.command()
@common_k8s_options
@click.option("-n", "--namespace", default="default", help="Kubernetes namespace")
@click.option(
    "-r",
    "--records",
    default=10,
    help="Number of records to show",
    required=False,
)
@click.option(
    "-w",
    "--watch",
    help="This will enable continuous running of this command, every given of seconds",
)
def show(context, namespace, records, watch):
    """
    This Lists all Pods in a given namespace, If not passed 'default' namespace will be used

    **Example Usage**:

    .. code-block:: shell

        $ hckr k8s show pods --namespace default

    **Command Reference**:
    """
    if context:
        info(f"Using context: {context}")
    info(f"Listing all Pods in namespace: {namespace}")
    if watch:
        info(f"Watch {colored('enabled', 'yellow')}, running this command every {watch} seconds")
        while True:
            list_pods(context, namespace, records)
            run_progress_barV2(int(watch))

    else:
        list_pods(context, namespace, records)
