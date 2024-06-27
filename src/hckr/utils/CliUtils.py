import logging

import requests
import rich
from packaging import version
from rich.panel import Panel

from .MessageUtils import colored, success, warning
from ..__about__ import __version__


def check_latest_version():
    current_version = __version__
    try:
        # latest stable version
        response = requests.get("https://pypi.org/pypi/hckr/json")
        latest_version = response.json()["info"]["version"]
        return is_new_version_available(current_version, latest_version), latest_version
    except requests.RequestException:
        return False, current_version


def is_new_version_available(current_version, latest_version):
    current_ver = version.parse(current_version)
    latest_ver = version.parse(latest_version)

    logging.debug(f"current : {current_version}, latest: {latest_version}")

    # Check if the latest version is greater than the current version
    return latest_ver > current_ver


def check_update(show_no_update=False):
    needs_update, latest_version = check_latest_version()
    if needs_update:
        warning(
            f"Info: Update available {colored(__version__, 'magenta')} ->  {colored(latest_version, 'green')}"
        )
        rich.print(
            Panel(
                "pip install --upgrade hckr",
                expand=False,
                title="Run to upgrade",
            )
        )
    elif show_no_update:
        success(
            f"Success: You are using latest version {colored(__version__, 'magenta')}"
        )
