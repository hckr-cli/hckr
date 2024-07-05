import logging
import sys
import threading

import pandas as pd
from kubernetes import stream
from kubernetes.client.exceptions import ApiException
from yaspin import yaspin

from hckr.utils.DataUtils import print_df_as_table
from hckr.utils.MessageUtils import error, info, colored
from hckr.utils.k8s.K8sUtils import _getApi, _human_readable_age

write_lock = threading.Lock()

def _getContainerName(coreApi, namespace, pod_name):
    pod = coreApi.read_namespaced_pod(name=pod_name, namespace=namespace)
    container_names = [container.name for container in pod.spec.containers]
    if container_names:
        if len(container_names) > 1:
            error(f"Multiple containers found. Please specify one using --container from the following containers: [yellow]{container_names}[/yellow]")
            exit(0)
        else:
            return container_names[0]
    else:
        error(f"No containers found in pod [yellow]{pod}[/yellow]")

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
                    "Age (↑)": _human_readable_age(pod.metadata.creation_timestamp),
                    # TODO: for some issue .metadata.creationTimestamp is different in kubectl and here
                    "Images": ", ".join(container_images),
                    "Containers": ", ".join([container.name for container in containers]),
                }
            )
        df = pd.DataFrame(pods_info)
        spinner.ok("✔")

    print_df_as_table(df, title=f"Pods in context: {currentContext}, namespace: {namespace}", count=count)

def delete_pod(context, namespace, pod_name):
    coreApi, currentContext = _getApi(context)
    try:
        info(
            f"Deleting pod {colored(pod_name, 'magenta')} in context: {colored(currentContext, 'yellow')}, namespace: {colored(namespace, 'yellow')}")
        coreApi.delete_namespaced_pod(name=pod_name, namespace=namespace)
        info(f"Pod {colored(pod_name, 'green')} deleted")
    except ApiException as e:
        error(f"Error while delete pod: {colored(pod_name, 'yellow')}: {e.reason}")
    except Exception as e:
        error(f"Error occurred\n {type(e)}")


def shell_into_pod(context, namespace, pod_name, container):
    coreApi, currentContext = _getApi(context)
    def read_stdin():
        while resp.is_open():
            try:
                data = sys.stdin.read(1)
                if data:
                    if data.strip() == 'exit':  # exit
                        break
                    resp.write_stdin(data)
            except KeyboardInterrupt:
                resp.close()
                print("\nSession closed by user.")
            except EOFError:
                break
            # finally:
            #     with write_lock:  # Ensure to lock before closing
            #         if resp.is_open():
            #             resp.close()

    info(
        f"Starting shell into pod {colored(pod_name, 'magenta')} in context: {colored(currentContext, 'yellow')}, namespace: {colored(namespace, 'yellow')}")
    try:
        if not container:
            logging.info("container is not defined, trying to get container name from pod")
            container = _getContainerName(coreApi, namespace, pod_name)
        exec_command = ['/bin/sh']

        with yaspin(text=f"Connecting to {container} in pod {pod_name}...", color="green", timer=True) as spinner:
            resp = stream.stream(coreApi.connect_get_namespaced_pod_exec,
                                 name=pod_name,
                                 namespace=namespace,
                                 command=exec_command,
                                 container=container,
                                 stderr=True,
                                 stdin=True,
                                 stdout=True,
                                 tty=True,
                                 _preload_content=False,
                                 _request_timeout=10 # time out for connection to container
                                 )
            spinner.ok("✔")
        info("You are now in the pod's shell. Type 'exit' or press 'CTRL-C' to end the session.")
        threading.Thread(target=read_stdin).start() # to start input thread
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
            resp.close()
            print("\nSession closed by user.")
        finally:
            with write_lock:
                if resp.is_open():
                    resp.close()
    except ApiException as e:
        error(f"Error connection to pod: {colored(pod_name, 'yellow')}\n {e.reason}")
    except Exception as e:
        error(f"Error occurred\n {type(e)}")
