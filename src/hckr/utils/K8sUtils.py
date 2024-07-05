from datetime import datetime, timezone

import pandas as pd
import rich
from kubernetes import client, config
from rich.panel import Panel
from yaspin import yaspin

from .DataUtils import print_df_as_table
from .MessageUtils import info, error


def _getApi(context):
    try:
        if context:
            config.load_kube_config(context=context)
            return client.CoreV1Api(), context
        else:
            config.load_kube_config()
            _, currentContext = config.list_kube_config_contexts()
            return client.CoreV1Api(), currentContext['name']
    except config.ConfigException as e:
        error(f"Error loading kube-config: \n{e}")
        exit(1)


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


def list_pods(context, namespace, count):
    with yaspin(text=f"Fetching pods for namespace {namespace}...", color="green", timer=True) as spinner:
        coreApi, currentContext = _getApi(context)
        ret = coreApi.list_namespaced_pod(namespace)
        sorted_pods = sorted(ret.items, key=lambda pod: pod.metadata.creation_timestamp, reverse=True)
        pods_info = []
        for pod in sorted_pods:  # get last count values
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
                }
            )
        df = pd.DataFrame(pods_info)
        spinner.ok("✔")

    print_df_as_table(df, title=f"Pods in context: {currentContext}, namespace: {namespace}", count=count)


def list_namespaces(context):
    coreApi = _getApi(context)
    ret = coreApi.list_namespace()
    rich.print(
        Panel(
            (
                "\n".join(i.metadata.name for i in ret.items)
                if len(ret.items) != 0
                else "NOTHING FOUND"
            ),
            expand=True,
            title=f"Namespaces in context: {context}",
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


def delete_pod(namespace, pod_name):
    coreApi = _getApi()
    info(f"Deleting pod {pod_name} in namespace {namespace}")
    coreApi.delete_namespaced_pod(name=pod_name, namespace=namespace)
    info(f"Pod {pod_name} deleted")

def list_contexts():
    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        rich.print("[red]Warning: No contexts found in kube-config file.[/red]")
        return

    context_names = [
        f"[green]{context['name']}[/green] <- [magenta]active[/magenta]" if context['name'] == active_context[
            'name'] else context['name']
        for context in contexts
    ]

    rich.print(
        Panel(
            "\n".join(context_names) if context_names else "NOTHING FOUND",
            expand=True,
            title="Contexts",
        )
    )
