import click

from ..k8s import k8s, common_k8s_options
from ...utils.CronUtils import run_progress_barV2
from ...utils.MessageUtils import info, colored
from ...utils.k8s.PodUtils import list_pods, delete_pod, shell_into_pod, get_pod_logs


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

        $ hckr k8s pod show --namespace default

    **Command Reference**:
    """
    if context:
        info(f"Using context: {context}")
    info(f"Listing all Pods in namespace: {namespace}")
    if watch:
        info(
            f"Watch {colored('enabled', 'yellow')}, running this command every {watch} seconds"
        )
        while True:
            list_pods(context, namespace, records)
            run_progress_barV2(int(watch))

    else:
        list_pods(context, namespace, records)


@pod.command()
@click.argument("pod_name")
@common_k8s_options
@click.option("-n", "--namespace", default="default", help="Kubernetes namespace")
def delete(context, namespace, pod_name):
    """
    Delete a pod in given namespace and context (default: current context)

    **Example Usage**:

    .. code-block:: shell

        $ hckr k8s pod delete <POD_NAME> --namespace default

    **Command Reference**:
    """
    if context:
        info(f"Using context: {context}")
    delete_pod(context, namespace, pod_name)


@pod.command()
@click.argument("pod_name")
@common_k8s_options
@click.option("-n", "--namespace", default="default", help="Kubernetes namespace")
@click.option(
    "--container",
    help="Kubernetes container to shell, If not provided hckr try to infer from pod",
)
def shell(context, namespace, pod_name, container):
    """
    Shell into a pod in the given namespace and context (default: current context)

    **Example Usage**:

    .. code-block:: shell

        $ hckr k8s pod shell <POD_NAME> --namespace default

    **Command Reference**:
    """
    if context:
        info(f"Using context: {context}")
    shell_into_pod(context, namespace, pod_name, container)


@pod.command()
@click.argument("pod_name")
@common_k8s_options
@click.option("-n", "--namespace", default="default", help="Kubernetes namespace")
@click.option(
    "--container",
    help="Kubernetes container to check logs, If not provided hckr try to infer from pod",
)
@click.option(
    "-w", "--watch", default=False, is_flag=True, help="Whether to watch/follow logs"
)
def logs(context, namespace, pod_name, container, watch):
    """
    Get logs from a pod in the given namespace and context (default: current context)

    **Example Usage**:

    .. code-block:: shell

        $ hckr k8s pod logs <POD_NAME> --namespace default

    **Command Reference**:
    """
    if context:
        info(f"Using context: {context}")
    get_pod_logs(context, namespace, pod_name, container, watch)
