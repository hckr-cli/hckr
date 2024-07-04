from datetime import datetime, timezone

import pandas as pd
import rich
from kubernetes import client, config, stream
from rich.panel import Panel

from .DataUtils import print_df_as_table
from .MessageUtils import info


def _getApi():
    config.load_kube_config()
    coreApi = client.CoreV1Api()
    return coreApi


def _human_readable_age(start_time):
    now = datetime.now(timezone.utc)
    delta = now - start_time

    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 0:
        return f"{days}d{hours}h"
    elif hours > 0:
        return f"{hours}h{minutes}m"
    else:
        return f"{minutes}m"


def list_pods(namespace):
    coreApi = _getApi()
    ret = coreApi.list_namespaced_pod(namespace)
    pods_info = []
    # print(ret.items[len(ret.items)-1].status)
    """
                   'state': {'running': {'started_at': datetime.datetime(2024, 6, 28, 9, 27, 8, tzinfo=tzutc())},
                                   'terminated': None,
                                   'waiting': None},

    """
    for pod in ret.items:
        containers = pod.spec.containers
        container_images = [container.image for container in containers]
        # print(pod.status.container_statuses)
        # FIX: THIS
        container_status = [x for x in pod.status.container_statuses if x.image in container_images]
        # print(container_status.image)
        pods_info.append({
            "Name": pod.metadata.name,
            "Status": pod.status.phase,
            # "Start Time": pod.status.start_time,
            "Age": pod.metadata.creation_timestamp,
            # TODO: for some issue .metadata.creationTimestamp is different in kubectl and here
            # "Containers": ", ".join([container.name for container in containers]),
            "Images": ", ".join(container_images),
            # "Restart Count": sum([container_state.restart_count for container_state in pod.status.container_statuses])
        })
    df = pd.DataFrame(pods_info)
    print_df_as_table(df, title=f"Pods in namespace: {namespace}", count=10)


def list_namespaces():
    coreApi = _getApi()
    ret = coreApi.list_namespace()
    rich.print(
        Panel(
            "\n".join(i.metadata.name for i in ret.items) if len(ret.items) != 0 else "NOTHING FOUND",
            expand=True,
            title="Namespaces",
        )
    )


def shell_into_pod(namespace, pod_name):
    coreApi = _getApi()
    info(f"Starting shell into pod {pod_name} in namespace {namespace}")
    exec_command = ['/bin/sh']
    resp = stream.stream(coreApi.connect_get_namespaced_pod_exec, pod_name, namespace,
                         command=exec_command, stderr=True, stdin=True,
                         stdout=True, tty=True)
    while resp.is_open():
        resp.update(timeout=1)
        if resp.peek_stdout():
            info(resp.read_stdout())
        if resp.peek_stderr():
            info(resp.read_stderr())


def delete_pod(namespace, pod_name):
    coreApi = _getApi()
    info(f"Deleting pod {pod_name} in namespace {namespace}")
    coreApi.delete_namespaced_pod(name=pod_name, namespace=namespace)
    info(f"Pod {pod_name} deleted")
