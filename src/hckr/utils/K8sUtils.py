from datetime import datetime, timezone

import pandas as pd
import rich
from kubernetes import client, config
from rich.panel import Panel

from .DataUtils import print_df_as_table

config.load_kube_config()
from yaspin import yaspin


def _getApi():
    coreApi = client.CoreV1Api()
    return coreApi


def _human_readable_age(start_time):
    now = datetime.now(timezone.utc)
    delta = now - start_time

    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days}d{hours}h"
    elif hours > 0:
        return f"{hours}h{minutes}m"
    elif minutes > 0:
        return f"{minutes}m{seconds}s"
    else:
        return f"{seconds}s"


def list_pods(namespace, count):
    with yaspin(text=f"Fetching pods for namespace {namespace}...", color="green") as spinner:
        coreApi = _getApi()
        ret = coreApi.list_namespaced_pod(namespace)
        sorted_pods = sorted(ret.items, key=lambda pod: pod.metadata.creation_timestamp)
        pods_info = []
        for pod in sorted_pods[-count:]:  # get last count values
            containers = pod.spec.containers
            container_images = [container.image for container in containers]
            pods_info.append(
                {
                    "Name": pod.metadata.name,
                    "Status": pod.status.phase,
                    # "Start Time": pod.status.start_time,
                    "Age": _human_readable_age(pod.metadata.creation_timestamp),
                    # TODO: for some issue .metadata.creationTimestamp is different in kubectl and here
                    # "Containers": ", ".join([container.name for container in containers]),
                    "Images": ", ".join(container_images),
                    # "Restart Count": sum([container_state.restart_count for container_state in pod.status.container_statuses])
                }
            )
        df = pd.DataFrame(pods_info)
        spinner.ok("✔")

    print_df_as_table(df, title=f"Pods in namespace: {namespace}", count=100)


def list_namespaces():
    coreApi = _getApi()
    ret = coreApi.list_namespace()
    rich.print(
        Panel(
            (
                "\n".join(i.metadata.name for i in ret.items)
                if len(ret.items) != 0
                else "NOTHING FOUND"
            ),
            expand=True,
            title="Namespaces",
        )
    )

# def shell_into_pod(namespace, pod_name):
#     coreApi = _getApi()
#     info(f"Starting shell into pod {pod_name} in namespace {namespace}")
#     exec_command = ['/bin/sh']
#     resp = stream.stream(coreApi.connect_get_namespaced_pod_exec, pod_name, namespace,
#                          command=exec_command, stderr=True, stdin=True,
#                          stdout=True, tty=True)
#     while resp.is_open():
#         resp.update(timeout=1)
#         if resp.peek_stdout():
#             info(resp.read_stdout())
#         if resp.peek_stderr():
#             info(resp.read_stderr())


# def delete_pod(namespace, pod_name):
#     coreApi = _getApi()
#     info(f"Deleting pod {pod_name} in namespace {namespace}")
#     coreApi.delete_namespaced_pod(name=pod_name, namespace=namespace)
#     info(f"Pod {pod_name} deleted")

def list_contexts():
    contexts, _ = config.list_kube_config_contexts()
    context_names = [context['name'] for context in contexts]
    for context in context_names:
        click.echo(context)
    return context_names

def switch_context(context_name):
    config.load_kube_config(context=context_name)
    global v1
    v1 = client.CoreV1Api()
    click.echo(f"Switched to context: {context_name}")
