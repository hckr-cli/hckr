import unittest
from datetime import datetime, timezone
from pathlib import Path  # type: ignore
from unittest.mock import patch, MagicMock  # type: ignore

import pyarrow as pa  # type: ignore
from click.testing import CliRunner
from kubernetes.client.models import V1Container
from pyarrow import parquet as pq  # type: ignore

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
        self.assertIn("Listing all contexts", result.output)
        self.assertIn("dev <- active", result.output)
        self.assertIn("prod", result.output)
