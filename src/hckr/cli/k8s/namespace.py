from ..k8s import k8s, common_k8s_options
from ...utils.k8s.K8sUtils import list_namespaces
from ...utils.MessageUtils import info


@k8s.group(
    help="List Kubernetes resources",
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
    if context:
        info(f"Using context: {context}")
    # info("Listing all namespaces")
    list_namespaces(context)

