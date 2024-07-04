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
def context():
    pass


@context.command()
def show():
    """
    This Command Lists all contexts available in kube config

    **Example Usage**:

    .. code-block:: shell

        $ hckr k8s show contexts

    **Command Reference**:
    """

    info("Listing all contexts")
    list_contexts()

