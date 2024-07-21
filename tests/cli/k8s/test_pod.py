import unittest
from pathlib import Path  # type: ignore
from unittest.mock import patch, MagicMock  # type: ignore

import pyarrow as pa  # type: ignore
from click.testing import CliRunner
from pyarrow import parquet as pq  # type: ignore

from hckr.cli.k8s.pod import show

parent_directory = Path(__file__).parent.parent


class TestK8sPodCLI(unittest.TestCase):
    @patch("hckr.utils.k8s.K8sUtils._getApi")
    def test_list_pods(self, mock_core_v1_api):
        runner = CliRunner()

        mock_api = MagicMock()
        mock_api.list_namespace.return_value = []
        mock_core_v1_api.return_value = (mock_api, "default")

        result = runner.invoke(show)
        print(result.output)
        assert "Listing all Pods in namespace: default" in result.output
