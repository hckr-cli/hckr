from ..k8s import k8s, common_k8s_options
from ...utils.k8s.K8sUtils import list_namespaces


@k8s.group(
    help="Kubernetes namespace related commands ",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def namespace():
    pass


@common_k8s_options
@namespace.command()
def show(context):
    """
    This Lists all namespaces available in given namespace, if not passed default context is used

    **Example Usage**:

    .. code-block:: shell

        $ hckr k8s show namespaces --context default

    **Command Reference**:
    """
    # info("Listing all namespaces")
    list_namespaces(context)
