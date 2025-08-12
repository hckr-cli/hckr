# TODO:FIX THE TESTS
# """
# Tests for Azure utility functions and CLI commands
# """
#
# import unittest
# from unittest.mock import Mock, patch, MagicMock
# from click.testing import CliRunner
# from hckr.utils.AzureUtils import (
#     AzureCredentials,
#     AzureConnectionTester,
#     test_azure_connection,
# )
# from hckr.cli.azure import azure, test_connection
#
#
# class TestAzureCredentials(unittest.TestCase):
#     """Test AzureCredentials dataclass"""
#
#     def test_azure_credentials_creation(self):
#         """Test basic credential creation"""
#         creds = AzureCredentials(tenant_id="test-tenant", client_id="test-client")
#
#         self.assertEqual(creds.tenant_id, "test-tenant")
#         self.assertEqual(creds.client_id, "test-client")
#         self.assertIsNone(creds.client_secret)
#         self.assertIsNone(creds.subscription_id)
#         self.assertIsNone(creds.resource_group)
#
#     def test_azure_credentials_with_all_fields(self):
#         """Test credential creation with all fields"""
#         creds = AzureCredentials(
#             tenant_id="test-tenant",
#             client_id="test-client",
#             client_secret="test-secret",
#             subscription_id="test-sub",
#             resource_group="test-rg",
#         )
#
#         self.assertEqual(creds.tenant_id, "test-tenant")
#         self.assertEqual(creds.client_id, "test-client")
#         self.assertEqual(creds.client_secret, "test-secret")
#         self.assertEqual(creds.subscription_id, "test-sub")
#         self.assertEqual(creds.resource_group, "test-rg")
#
#
# class TestAzureConnectionTester(unittest.TestCase):
#     """Test AzureConnectionTester class"""
#
#     def setUp(self):
#         """Set up test fixtures"""
#         self.tester = AzureConnectionTester()
#         self.valid_creds = AzureCredentials(
#             tenant_id="test-tenant-id",
#             client_id="test-client-id",
#             client_secret="test-client-secret",
#         )
#
#     def test_init_with_default_logger(self):
#         """Test initialization with default logger"""
#         tester = AzureConnectionTester()
#         self.assertIsNotNone(tester.logger)
#
#     def test_init_with_custom_logger(self):
#         """Test initialization with custom logger"""
#         mock_logger = Mock()
#         tester = AzureConnectionTester(mock_logger)
#         self.assertEqual(tester.logger, mock_logger)
#
#     @patch("hckr.utils.AzureUtils.ClientSecretCredential")
#     @patch("hckr.utils.AzureUtils.ResourceManagementClient")
#     def test_missing_azure_sdk(self, mock_resource_client, mock_credential):
#         """Test behavior when Azure SDK is not installed"""
#         with patch(
#             "hckr.utils.AzureUtils.ClientSecretCredential",
#             side_effect=ImportError("No module named 'azure'"),
#         ):
#             success, result = self.tester.test_connection(self.valid_creds)
#
#             self.assertFalse(success)
#             self.assertIn("Azure SDK not installed", result["errors"][0])
#             self.assertIn("pip install azure-identity", result["message"])
#
#     def test_missing_required_credentials(self):
#         """Test validation of required credentials"""
#         # Test missing tenant_id
#         invalid_creds = AzureCredentials(tenant_id="", client_id="test-client")
#         success, result = self.tester.test_connection(invalid_creds)
#
#         self.assertFalse(success)
#         self.assertIn("Missing required credentials", result["errors"][0])
#
#         # Test missing client_id
#         invalid_creds = AzureCredentials(tenant_id="test-tenant", client_id="")
#         success, result = self.tester.test_connection(invalid_creds)
#
#         self.assertFalse(success)
#         self.assertIn("Missing required credentials", result["errors"][0])
#
#     def test_missing_client_secret(self):
#         """Test behavior when client_secret is missing"""
#         creds_no_secret = AzureCredentials(
#             tenant_id="test-tenant", client_id="test-client"
#         )
#
#         success, result = self.tester.test_connection(creds_no_secret)
#
#         self.assertFalse(success)
#         self.assertIn("Client secret is required", result["errors"][0])
#
#     @patch("hckr.utils.AzureUtils.ClientSecretCredential")
#     @patch("hckr.utils.AzureUtils.ResourceManagementClient")
#     def test_successful_authentication_only(
#         self, mock_resource_client, mock_credential
#     ):
#         """Test successful authentication without subscription access"""
#         # Mock successful credential creation and token acquisition
#         mock_cred_instance = Mock()
#         mock_token = Mock()
#         mock_token.expires_on = 1234567890
#         mock_cred_instance.get_token.return_value = mock_token
#         mock_credential.return_value = mock_cred_instance
#
#         success, result = self.tester.test_connection(self.valid_creds)
#
#         self.assertTrue(success)
#         self.assertEqual(result["message"], "Azure connection test successful")
#         self.assertTrue(result["details"]["token_acquired"])
#         self.assertEqual(result["details"]["auth_method"], "Service Principal")
#         self.assertEqual(result["details"]["tenant_id"], "test-tenant-id")
#         self.assertEqual(result["details"]["client_id"], "test-client-id")
#
#     @patch("hckr.utils.AzureUtils.ClientSecretCredential")
#     @patch("hckr.utils.AzureUtils.ResourceManagementClient")
#     def test_authentication_failure(self, mock_resource_client, mock_credential):
#         """Test authentication failure"""
#         # Mock credential creation but token acquisition failure
#         mock_cred_instance = Mock()
#         mock_cred_instance.get_token.side_effect = Exception("Invalid credentials")
#         mock_credential.return_value = mock_cred_instance
#
#         success, result = self.tester.test_connection(self.valid_creds)
#
#         self.assertFalse(success)
#         self.assertEqual(result["message"], "Authentication failed")
#         self.assertIn("Failed to acquire access token", result["errors"][0])
#
#     @patch("hckr.utils.AzureUtils.ClientSecretCredential")
#     @patch("hckr.utils.AzureUtils.ResourceManagementClient")
#     def test_subscription_access_success(self, mock_resource_client, mock_credential):
#         """Test successful subscription access"""
#         # Mock successful authentication
#         mock_cred_instance = Mock()
#         mock_token = Mock()
#         mock_token.expires_on = 1234567890
#         mock_cred_instance.get_token.return_value = mock_token
#         mock_credential.return_value = mock_cred_instance
#
#         # Mock successful resource client
#         mock_resource_instance = Mock()
#         mock_rg1 = Mock()
#         mock_rg1.name = "rg1"
#         mock_rg2 = Mock()
#         mock_rg2.name = "rg2"
#         mock_resource_instance.resource_groups.list.return_value = [mock_rg1, mock_rg2]
#         mock_resource_client.return_value = mock_resource_instance
#
#         creds_with_sub = AzureCredentials(
#             tenant_id="test-tenant-id",
#             client_id="test-client-id",
#             client_secret="test-client-secret",
#             subscription_id="test-subscription-id",
#         )
#
#         success, result = self.tester.test_connection(creds_with_sub)
#
#         self.assertTrue(success)
#         self.assertTrue(result["details"]["subscription_access"])
#         self.assertEqual(result["details"]["resource_groups_count"], 2)
#         self.assertEqual(result["details"]["subscription_id"], "test-subscription-id")
#
#     @patch("hckr.utils.AzureUtils.ClientSecretCredential")
#     @patch("hckr.utils.AzureUtils.ResourceManagementClient")
#     def test_resource_group_access_success(self, mock_resource_client, mock_credential):
#         """Test successful resource group access"""
#         # Mock successful authentication
#         mock_cred_instance = Mock()
#         mock_token = Mock()
#         mock_token.expires_on = 1234567890
#         mock_cred_instance.get_token.return_value = mock_token
#         mock_credential.return_value = mock_cred_instance
#
#         # Mock successful resource client with specific RG access
#         mock_resource_instance = Mock()
#         mock_resource_instance.resource_groups.list.return_value = []
#
#         mock_rg = Mock()
#         mock_rg.location = "eastus"
#         mock_resource_instance.resource_groups.get.return_value = mock_rg
#         mock_resource_client.return_value = mock_resource_instance
#
#         creds_with_rg = AzureCredentials(
#             tenant_id="test-tenant-id",
#             client_id="test-client-id",
#             client_secret="test-client-secret",
#             subscription_id="test-subscription-id",
#             resource_group="test-rg",
#         )
#
#         success, result = self.tester.test_connection(creds_with_rg)
#
#         self.assertTrue(success)
#         self.assertTrue(result["details"]["resource_group_access"])
#         self.assertEqual(result["details"]["resource_group_location"], "eastus")
#
#     def test_test_connection_simple(self):
#         """Test the simplified connection test method"""
#         with patch.object(self.tester, "test_connection") as mock_test:
#             mock_test.return_value = (True, {"message": "success"})
#
#             success, result = self.tester.test_connection_simple(
#                 tenant_id="test-tenant",
#                 client_id="test-client",
#                 client_secret="test-secret",
#                 subscription_id="test-sub",
#                 resource_group="test-rg",
#             )
#
#             self.assertTrue(success)
#             self.assertEqual(result["message"], "success")
#
#             # Verify the credentials were created correctly
#             call_args = mock_test.call_args[0][0]
#             self.assertEqual(call_args.tenant_id, "test-tenant")
#             self.assertEqual(call_args.client_id, "test-client")
#             self.assertEqual(call_args.client_secret, "test-secret")
#             self.assertEqual(call_args.subscription_id, "test-sub")
#             self.assertEqual(call_args.resource_group, "test-rg")
#
#
# class TestAzureConnectionFunction(unittest.TestCase):
#     """Test the convenience function"""
#
#     @patch("hckr.utils.AzureUtils.AzureConnectionTester")
#     def test_test_azure_connection_function(self, mock_tester_class):
#         """Test the convenience function"""
#         # Mock the tester instance
#         mock_tester = Mock()
#         mock_tester.test_connection_simple.return_value = (True, {"message": "success"})
#         mock_tester_class.return_value = mock_tester
#
#         success, result = test_azure_connection(
#             tenant_id="test-tenant",
#             client_id="test-client",
#             client_secret="test-secret",
#         )
#
#         self.assertTrue(success)
#         self.assertEqual(result["message"], "success")
#
#         # Verify the tester was called correctly
#         mock_tester.test_connection_simple.assert_called_once_with(
#             "test-tenant", "test-client", "test-secret", None, None
#         )
#
#
# class TestAzureCLI(unittest.TestCase):
#     """Test Azure CLI commands directly using CliRunner"""
#
#     def test_azure_group_command(self):
#         """Test the azure command group help"""
#         runner = CliRunner()
#         result = runner.invoke(azure, ["--help"])
#         print(result.output)
#         self.assertEqual(result.exit_code, 0)
#         self.assertIn("Azure utility commands", result.output)
#         self.assertIn("test-connection", result.output)
#
#     @patch("hckr.cli.azure.test_azure_connection")
#     def test_azure_test_connection_cli_success(self, mock_test_connection):
#         """Test azure test-connection CLI command with successful result"""
#         # Mock successful connection test
#         mock_test_connection.return_value = (
#             True,
#             {
#                 "message": "Azure connection test successful",
#                 "details": {
#                     "tenant_id": "test-tenant",
#                     "client_id": "test-client",
#                     "auth_method": "Service Principal",
#                     "token_acquired": True,
#                     "token_expires": 1234567890
#                 }
#             }
#         )
#
#         runner = CliRunner()
#         result = runner.invoke(
#             test_connection,
#             [
#                 "--tenant-id", "test-tenant",
#                 "--client-id", "test-client",
#                 "--client-secret", "test-secret"
#             ],
#             input="test-secret\n"  # Provide input for the password prompt
#         )
#
#         print(result.output)
#         self.assertEqual(result.exit_code, 0)
#         self.assertIn("✅ SUCCESS", result.output)
#         self.assertIn("Azure Connection Test Results", result.output)
#         self.assertIn("Service Principal", result.output)
#
#         # Verify the underlying function was called with correct parameters
#         mock_test_connection.assert_called_once_with(
#             tenant_id="test-tenant",
#             client_id="test-client",
#             client_secret="test-secret",
#             subscription_id=None,
#             resource_group=None
#         )
#
#     @patch("hckr.cli.azure.test_azure_connection")
#     def test_azure_test_connection_cli_with_subscription(self, mock_test_connection):
#         """Test azure test-connection CLI command with subscription and resource group"""
#         # Mock successful connection test with subscription access
#         mock_test_connection.return_value = (
#             True,
#             {
#                 "message": "Azure connection test successful with subscription access",
#                 "details": {
#                     "tenant_id": "test-tenant",
#                     "client_id": "test-client",
#                     "auth_method": "Service Principal",
#                     "token_acquired": True,
#                     "subscription_access": True,
#                     "subscription_id": "test-sub",
#                     "resource_groups_count": 5,
#                     "resource_group_access": True,
#                     "resource_group_location": "eastus"
#                 }
#             }
#         )
#
#         runner = CliRunner()
#         result = runner.invoke(
#             test_connection,
#             [
#                 "--tenant-id", "test-tenant",
#                 "--client-id", "test-client",
#                 "--client-secret", "test-secret",
#                 "--subscription-id", "test-sub",
#                 "--resource-group", "test-rg"
#             ],
#             input="test-secret\n"
#         )
#
#         print(result.output)
#         self.assertEqual(result.exit_code, 0)
#         self.assertIn("✅ SUCCESS", result.output)
#         self.assertIn("Subscription Access", result.output)
#         self.assertIn("Resource Groups Found", result.output)
#         self.assertIn("Resource Group Access", result.output)
#
#         mock_test_connection.assert_called_once_with(
#             tenant_id="test-tenant",
#             client_id="test-client",
#             client_secret="test-secret",
#             subscription_id="test-sub",
#             resource_group="test-rg"
#         )
#
#     @patch("hckr.cli.azure.test_azure_connection")
#     def test_azure_test_connection_cli_failure(self, mock_test_connection):
#         """Test azure test-connection CLI command with failure result"""
#         # Mock failed connection test
#         mock_test_connection.return_value = (
#             False,
#             {
#                 "message": "Authentication failed",
#                 "errors": ["Invalid credentials provided"],
#                 "details": {}
#             }
#         )
#
#         runner = CliRunner()
#         result = runner.invoke(
#             test_connection,
#             [
#                 "--tenant-id", "test-tenant",
#                 "--client-id", "test-client",
#                 "--client-secret", "invalid-secret"
#             ],
#             input="invalid-secret\n"
#         )
#
#         print(result.output)
#         self.assertEqual(result.exit_code, 1)  # Should exit with error code
#         self.assertIn("❌ FAILED", result.output)
#         self.assertIn("Authentication failed", result.output)
#         self.assertIn("Invalid credentials provided", result.output)
#
#     def test_azure_test_connection_cli_missing_required_args(self):
#         """Test azure test-connection CLI command with missing required arguments"""
#         runner = CliRunner()
#
#         # Test missing tenant-id
#         result = runner.invoke(test_connection, ["--client-id", "test-client"])
#         print(result.output)
#         self.assertNotEqual(result.exit_code, 0)
#         self.assertTrue("Missing option" in result.output or "Error" in result.output)
#
#         # Test missing client-id
#         result = runner.invoke(test_connection, ["--tenant-id", "test-tenant"])
#         print(result.output)
#         self.assertNotEqual(result.exit_code, 0)
#         self.assertTrue("Missing option" in result.output or "Error" in result.output)
#
#
# if __name__ == "__main__":
#     unittest.main()
