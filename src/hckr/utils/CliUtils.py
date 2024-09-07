import logging

import requests
import rich
from packaging import version
from rich.panel import Panel

from .MessageUtils import colored, success, warning
from .config.Constants import SENTRY_DSN
from ..__about__ import __version__
import platform


LOGGING_LEVELS = {
    0: logging.NOTSET,
    # 1: logging.ERROR,
    # 2: logging.WARN,
    1: logging.INFO,
    2: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


# Define a format for the console handler
class Info:
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0


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
                title="Run to upgrade using Pip",
            )
        )
        # only show this on MacOs
        if platform.system() == "Darwin":
            rich.print(
                Panel(
                    "brew update && brew upgrade hckr",
                    expand=False,
                    title="Run to upgrade using Homebrew",
                )
            )
    elif show_no_update:
        success(
            f"Success: You are using latest version {colored(__version__, 'magenta')}"
        )


def sentry_init():
    import sentry_sdk

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )
