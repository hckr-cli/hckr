import unittest
from datetime import datetime, timezone
from pathlib import Path  # type: ignore
from unittest.mock import patch, MagicMock  # type: ignore

import pyarrow as pa  # type: ignore
from click.testing import CliRunner
from kubernetes.client.models import V1Container
from pyarrow import parquet as pq  # type: ignore

from hckr.cli.k8s.namespace import show

parent_directory = Path(__file__).parent.parent


class TestK8sNamespaceCLI(unittest.TestCase):
    @patch("hckr.utils.k8s.K8sUtils._getApi")
    def test_list_namespaces_default_context(self, mock_core_v1_api):
        runner = CliRunner()
        mock_api = MagicMock()
        mock_api.list_namespace.return_value = []
        mock_core_v1_api.return_value = (mock_api, "default")

        result = runner.invoke(show)
        print(result.output)
        assert "Using default context: default" in result.output

    @patch("hckr.utils.k8s.K8sUtils._getApi")
    def test_list_namespaces_given_context(self, mock_core_v1_api):
        runner = CliRunner()
        mock_api = MagicMock()
        mock_api.list_namespace.return_value = []
        mock_core_v1_api.return_value = (mock_api, "default")

        result = runner.invoke(show, ['--context', 'mycontext'])
        print(result.output)
        assert "Using given context: mycontext" in result.output
