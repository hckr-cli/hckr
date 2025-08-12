"""
Azure Connection Testing Utility

This module provides utilities to test Azure connections with different authentication methods.
"""

import logging
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class AzureCredentials:
    """Data class to hold Azure credentials"""
    tenant_id: str
    client_id: str
    client_secret: Optional[str] = None
    subscription_id: Optional[str] = None
    resource_group: Optional[str] = None


class AzureConnectionTester:
    """Utility class for testing Azure connections"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)

    def test_connection(self, credentials: AzureCredentials) -> Tuple[bool, Dict[str, Any]]:
        """
        Test Azure connection using provided credentials
        
        Args:
            credentials: AzureCredentials object containing authentication details
            
        Returns:
            Tuple of (success: bool, result: dict) where result contains
            connection details or error information
        """
        result = {
            "success": False,
            "message": "",
            "details": {},
            "errors": []
        }

        try:
            # Try to import Azure SDK
            try:
                from azure.identity import ClientSecretCredential
                from azure.mgmt.resource import ResourceManagementClient
            except ImportError as e:
                result["errors"].append(f"Azure SDK not installed: {str(e)}")
                result["message"] = "Azure SDK packages are required. Install with: pip install azure-identity azure-mgmt-resource"
                return False, result

            # Validate required credentials
            if not all([credentials.tenant_id, credentials.client_id]):
                result["errors"].append("Missing required credentials: tenant_id and client_id are required")
                result["message"] = "Invalid credentials provided"
                return False, result

            # Test authentication
            self.logger.info("Testing Azure authentication...")
            
            if credentials.client_secret:
                # Service Principal authentication
                credential = ClientSecretCredential(
                    tenant_id=credentials.tenant_id,
                    client_id=credentials.client_id,
                    client_secret=credentials.client_secret
                )
                result["details"]["auth_method"] = "Service Principal"
            else:
                result["errors"].append("Client secret is required for service principal authentication")
                result["message"] = "Missing client_secret for authentication"
                return False, result

            # Test connection by getting an access token
            try:
                token = credential.get_token("https://management.azure.com/.default")
                result["details"]["token_acquired"] = True
                result["details"]["token_expires"] = token.expires_on
                self.logger.info("Successfully acquired Azure access token")
            except Exception as e:
                result["errors"].append(f"Failed to acquire access token: {str(e)}")
                result["message"] = "Authentication failed"
                return False, result

            # If subscription_id is provided, test resource management access
            if credentials.subscription_id:
                try:
                    resource_client = ResourceManagementClient(credential, credentials.subscription_id)
                    
                    # Test by listing resource groups (this requires minimal permissions)
                    resource_groups = list(resource_client.resource_groups.list())
                    result["details"]["subscription_access"] = True
                    result["details"]["resource_groups_count"] = len(resource_groups)
                    result["details"]["subscription_id"] = credentials.subscription_id
                    
                    if credentials.resource_group:
                        # Test specific resource group access
                        try:
                            rg = resource_client.resource_groups.get(credentials.resource_group)
                            result["details"]["resource_group_access"] = True
                            result["details"]["resource_group_location"] = rg.location
                        except Exception as e:
                            result["errors"].append(f"Resource group access failed: {str(e)}")
                    
                    self.logger.info(f"Successfully connected to subscription: {credentials.subscription_id}")
                    
                except Exception as e:
                    result["errors"].append(f"Resource management access failed: {str(e)}")
                    result["details"]["subscription_access"] = False

            result["success"] = True
            result["message"] = "Azure connection test successful"
            result["details"]["tenant_id"] = credentials.tenant_id
            result["details"]["client_id"] = credentials.client_id

            return True, result

        except Exception as e:
            result["errors"].append(f"Unexpected error during connection test: {str(e)}")
            result["message"] = "Connection test failed due to unexpected error"
            self.logger.error(f"Azure connection test failed: {str(e)}", exc_info=True)
            return False, result

    def test_connection_simple(
        self, 
        tenant_id: str, 
        client_id: str, 
        client_secret: str,
        subscription_id: Optional[str] = None,
        resource_group: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Simplified method to test Azure connection with individual parameters
        
        Args:
            tenant_id: Azure tenant ID
            client_id: Azure client ID (application ID)
            client_secret: Azure client secret
            subscription_id: Optional Azure subscription ID
            resource_group: Optional resource group name
            
        Returns:
            Tuple of (success: bool, result: dict)
        """
        credentials = AzureCredentials(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            subscription_id=subscription_id,
            resource_group=resource_group
        )
        
        return self.test_connection(credentials)


def test_azure_connection(
    tenant_id: str,
    client_id: str, 
    client_secret: str,
    subscription_id: Optional[str] = None,
    resource_group: Optional[str] = None,
    logger: Optional[logging.Logger] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Convenience function to test Azure connection
    
    Args:
        tenant_id: Azure tenant ID
        client_id: Azure client ID (application ID)
        client_secret: Azure client secret
        subscription_id: Optional Azure subscription ID
        resource_group: Optional resource group name
        logger: Optional logger instance
        
    Returns:
        Tuple of (success: bool, result: dict) where result contains
        connection details or error information
    """
    tester = AzureConnectionTester(logger)
    return tester.test_connection_simple(
        tenant_id, client_id, client_secret, subscription_id, resource_group
    )