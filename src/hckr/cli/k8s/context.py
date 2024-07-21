from ..k8s import k8s
from ...utils.MessageUtils import info
from ...utils.k8s.K8sUtils import list_contexts


@k8s.group(
    help="Kubernetes context related commands ",
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
