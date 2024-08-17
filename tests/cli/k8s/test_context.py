import unittest
from pathlib import Path  # type: ignore
from unittest.mock import patch, MagicMock  # type: ignore

from click.testing import CliRunner

from hckr.cli.k8s.context import show

parent_directory = Path(__file__).parent.parent


class TestK8sContextCLI(unittest.TestCase):
    @patch("kubernetes.config.list_kube_config_contexts")
    def test_list_contexts(self, mock_config_list_context):
        runner = CliRunner()

        # mocking
        contexts = [
            {"name": "dev"},
            {"name": "prod"},
        ]
        active_context = {"name": "dev"}
        mock_config_list_context.return_value = (contexts, active_context)

        result = runner.invoke(show)
        print(result.output)
        # self.assertEqual(result.exit_code, 0)
        assert "Listing all contexts" in result.output
        assert "dev <- active" in result.output
        assert "prod" in result.output
