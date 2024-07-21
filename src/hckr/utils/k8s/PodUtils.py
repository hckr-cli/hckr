import logging
import re
import sys
import threading

import pandas as pd
import rich
from kubernetes import stream, watch  # type: ignore
from kubernetes.client.exceptions import ApiException  # type: ignore
from yaspin import yaspin  # type: ignore

from hckr.utils.DataUtils import print_df_as_table
from hckr.utils.MessageUtils import error, info, colored, warning, success
from hckr.utils.k8s.K8sUtils import _getApi, _human_readable_age
import logging


def _getContainerName(coreApi, namespace, pod_name):
    pod = coreApi.read_namespaced_pod(name=pod_name, namespace=namespace)
    container_names = [container.name for container in pod.spec.containers]
    if container_names:
        if len(container_names) > 1:
            error(f"Error: Multiple containers found for pod {pod_name}")
            warning(
                f"Please specify one using --container from the following containers: [magenta]{container_names}"
            )
            exit(0)
        else:
            return container_names[0]
    else:
        error(f"No containers found in pod [yellow]{pod}[/yellow]")


def list_pods(context, namespace, count):
    with yaspin(
        text=f"Fetching pods for namespace {namespace}...", color="green", timer=True
    ) as spinner:
        coreApi, currentContext = _getApi(context)
        ret = coreApi.list_namespaced_pod(namespace)
        sorted_pods = sorted(
            ret.items, key=lambda pod: pod.metadata.creation_timestamp, reverse=True
        )
        pods_info = []
        for pod in sorted_pods:  # get last count values
            containers = pod.spec.containers
            container_images = [container.image for container in containers]
            pods_info.append(
                {
                    "Name": pod.metadata.name,
                    "Status": pod.status.phase,
                    # "Start Time": pod.status.start_time,
                    "Age (↑)": _human_readable_age(pod.metadata.creation_timestamp),
                    # TODO: for some issue .metadata.creationTimestamp is different in kubectl and here
                    "Images": ", ".join(container_images),
                    "Containers": ", ".join(
                        [container.name for container in containers]
                    ),
                }
            )
        df = pd.DataFrame(pods_info)
        spinner.ok("✔")

    print_df_as_table(
        df,
        title=f"Pods in context: {currentContext}, namespace: {namespace}",
        count=count,
    )


def delete_pod(context, namespace, pod_name):
    coreApi, currentContext = _getApi(context)
    try:
        info(
            f"Deleting pod {colored(pod_name, 'magenta')} in context: {colored(currentContext, 'yellow')}, namespace: {colored(namespace, 'yellow')}"
        )
        coreApi.delete_namespaced_pod(name=pod_name, namespace=namespace)
        info(f"Pod {colored(pod_name, 'green')} deleted")
    except ApiException as e:
        error(f"Error while delete pod: {colored(pod_name, 'yellow')}: {e.reason}")
    except Exception as e:
        error(f"Error occurred\n {type(e)}")


def shell_into_pod(context, namespace, pod_name, container):
    coreApi, currentContext = _getApi(context)

    def read_stdin():
        try:
            while resp.is_open():
                data = sys.stdin.read(1)
                if data:
                    if resp.is_open():
                        resp.write_stdin(data)
        except KeyboardInterrupt as e:
            logging.info(f"Closing web socket: {e}")
            success("Session closed by user.")
        except EOFError as e:
            logging.info(f"End of file occurred: {e}")
            error(f"End of file occurred\n{e}")

    info(
        f"Starting shell into pod {colored(pod_name, 'magenta')} in context: {colored(currentContext, 'yellow')}, namespace: {colored(namespace, 'yellow')}"
    )
    try:
        if not container:
            logging.info(
                "container is not defined, trying to get container name from pod"
            )
            container = _getContainerName(coreApi, namespace, pod_name)
        exec_command = ["/bin/sh"]

        with yaspin(
            text=f"Connecting to {container} in pod {pod_name}...",
            color="green",
            timer=True,
        ) as spinner:
            resp = stream.stream(
                coreApi.connect_get_namespaced_pod_exec,
                name=pod_name,
                namespace=namespace,
                command=exec_command,
                container=container,
                stderr=True,
                stdin=True,
                stdout=True,
                tty=True,
                _preload_content=False,
                _request_timeout=10,  # time out for connection to container
            )
            spinner.ok("✔")
        info(
            f"You are now in the {colored(container, 'magenta')} shell. Type 'exit' or press 'CTRL-C' to end the session.\n\n"
        )
        threading.Thread(target=read_stdin).start()  # to start input thread
        try:
            while resp.is_open():
                resp.update(timeout=1)
                if resp.peek_stdout():
                    output = resp.read_stdout()
                    sys.stdout.write(output)
                    sys.stdout.flush()
                if resp.peek_stderr():
                    error_output = resp.read_stderr()
                    sys.stderr.write(error_output)
                    sys.stderr.flush()
        except KeyboardInterrupt:
            rich.print("\n[green]Session closed by user.")
        finally:
            if resp.is_open():
                logging.info("Closing web socket")
                resp.close()
    except ApiException as e:
        error(f"Error connection to pod: {colored(pod_name, 'yellow')}\n {e.reason}")
    except Exception as e:
        error(f"Unexpected error occurred: {e}")


def get_pod_logs(context, namespace, pod_name, container, follow):
    coreApi, currentContext = _getApi(context)
    tail_lines = 10

    info(
        f"Getting logs from pod {colored(pod_name, 'magenta')}, container: {container} in context: {colored(currentContext, 'yellow')}, namespace: {colored(namespace, 'yellow')}"
    )
    if follow:
        info("watch is enabled")
    else:
        info("watch is disabled")
    if not container:
        logging.info("container is not defined, trying to get container name from pod")
        container = _getContainerName(coreApi, namespace, pod_name)
        logging.info(f"container is {container}")

    try:
        # Set up streaming of logs if follow is True
        if follow:
            w = watch.Watch()
            try:
                for log_entry in w.stream(
                    coreApi.read_namespaced_pod_log,
                    name=pod_name,
                    namespace=namespace,
                    container=container,
                    tail_lines=tail_lines,
                ):
                    print(log_entry)
            finally:
                w.stop()
        else:
            # Retrieve logs without following (static)
            logs = coreApi.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                container=container,
                follow=follow,
                tail_lines=tail_lines,
            )
            print(logs)
    except ApiException as e:
        error(f"An exception occurred while reading log: {e}")
        return None
