import unittest
from datetime import datetime, timezone
from pathlib import Path  # type: ignore
from unittest.mock import patch, MagicMock  # type: ignore

import pyarrow as pa  # type: ignore
from click.testing import CliRunner
from pyarrow import parquet as pq  # type: ignore
from hckr.cli.k8s.show import pods, namespaces
from hckr.cli import cli

parent_directory = Path(__file__).parent.parent


class TestK8sCLI(unittest.TestCase):
    @patch('hckr.k8s_utils.client.CoreV1Api')
    @patch('hckr.k8s_utils.config.load_kube_config')
    def test_list_pods(self, mock_load_kube_config, mock_core_v1_api):
        runner = CliRunner()

        # Setup mock return values
        mock_pod = MagicMock()
        mock_pod.metadata.name = 'mock-pod'
        mock_pod.status.phase = 'Running'
        mock_pod.spec.node_name = 'mock-node'
        mock_pod.metadata.creation_timestamp = datetime.now(timezone.utc)
        mock_pod.status.container_statuses = []

        mock_core_v1_api.return_value.list_namespaced_pod.return_value.items = [mock_pod]

        result = runner.invoke(pods, ['--namespace', 'default'])

        self.assertEqual(result.exit_code, 0)
        self.assertIn('mock-pod', result.output)

    @patch('kubernetes.config.load_config')
    @patch('kubernetes.client.api.core_v1_api.CoreV1Api')
    def test_list_namespaces(self, mock_load_kube_config, mock_core_v1_api):
        runner = CliRunner()

        # Setup mock return values
        mock_namespace = MagicMock()
        mock_namespace.metadata.name = 'mock-namespace'

        mock_core_v1_api.return_value.list_namespace.return_value.items = [mock_namespace]

        result = runner.invoke(namespaces, [])
        print(result.output)
        self.assertEqual(result.exit_code, 0)
        self.assertIn('mock-namespace', result.output)

    @patch('hckr.k8s_utils.client.CoreV1Api')
    @patch('hckr.k8s_utils.config.load_kube_config')
    def test_delete_pod(self, mock_load_kube_config, mock_core_v1_api):
        runner = CliRunner()

        result = runner.invoke(cli, ['k8s', 'delete', '--namespace', 'default', 'mock-pod'])

        self.assertEqual(result.exit_code, 0)
        mock_core_v1_api.return_value.delete_namespaced_pod.assert_called_with(name='mock-pod', namespace='default')


if __name__ == "__main__":
    unittest.main()
