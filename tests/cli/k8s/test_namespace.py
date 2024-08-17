import unittest
from pathlib import Path  # type: ignore
from unittest.mock import patch, MagicMock  # type: ignore

from click.testing import CliRunner

from hckr.cli.k8s.namespace import show


class TestK8sNamespaceCLI(unittest.TestCase):
    @patch("hckr.utils.k8s.K8sUtils._getApi")
    def test_list_namespaces_default_context(self, mock_core_v1_api):
        runner = CliRunner()

        # Create namespace mock objects with correct return values for the name property
        namespace1 = MagicMock()
        namespace1.metadata.name = "test_namespace"

        # Set up the MagicMock for the API client
        mock_api = MagicMock()
        mock_api.list_namespace.return_value = MagicMock(items=[namespace1])

        mock_core_v1_api.return_value = (mock_api, "default")

        result = runner.invoke(show)
        print(result.output)
        assert "Using default context: default" in result.output
        assert "test_namespace" in result.output

    @patch("hckr.utils.k8s.K8sUtils._getApi")
    def test_list_namespaces_given_context(self, mock_core_v1_api):
        runner = CliRunner()
        mock_api = MagicMock()
        mock_api.list_namespace.return_value = []
        mock_core_v1_api.return_value = (mock_api, "default")

        result = runner.invoke(show, ["--context", "mycontext"])
        print(result.output)
        assert "Using given context: mycontext" in result.output
