from datetime import datetime, timezone

import rich
from kubernetes import client, config  # type: ignore
from rich.panel import Panel

from ..MessageUtils import error, info


def _getApi(context):
    try:
        if context:
            config.load_kube_config(context=context)
            return client.CoreV1Api(), context
        else:
            config.load_kube_config()
            _, currentContext = config.list_kube_config_contexts()
            return client.CoreV1Api(), currentContext["name"]
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


def list_namespaces(context):
    coreApi, currentContext = _getApi(context)
    if context:
        info(f"Using given context: {context}")
    else:
        info(f"Using default context: {currentContext}")

    ret = coreApi.list_namespace()
    rich.print(
        Panel(
            (
                "\n".join(i.metadata.name for i in ret.items)
                if len(ret.items) != 0
                else "NOTHING FOUND"
            ),
            expand=True,
            title=f"Namespaces in context: {currentContext}",
        )
    )


def list_contexts():
    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        rich.print("[red]Warning: No contexts found in kube-config file.[/red]")
        return

    context_names = [
        (
            f"[green]{context['name']}[/green] <- [magenta]active[/magenta]"
            if context["name"] == active_context["name"]
            else context["name"]
        )
        for context in contexts
    ]

    rich.print(
        Panel(
            "\n".join(context_names) if context_names else "NOTHING FOUND",
            expand=True,
            title="Contexts",
        )
    )
