import unittest
from pathlib import Path  # type: ignore
from unittest.mock import patch, MagicMock  # type: ignore

from click.testing import CliRunner

from hckr.cli.k8s.pod import show


class TestK8sPodCLI(unittest.TestCase):

    # note - we have to patch wherever this is used not wherever it is defined
    @patch("hckr.utils.k8s.PodUtils._getApi")
    def test_list_pods(self, mock_core_v1_api):
        runner = CliRunner()

        mock_api = MagicMock()
        mock_api.list_namespaced_pod.return_value = MagicMock(items=[])

        mock_core_v1_api.return_value = (mock_api, "default")

        result = runner.invoke(show)
        print(result.output)
        assert "Listing all Pods in namespace: default" in result.output


# TODO: add tests for delete, logs etc.
