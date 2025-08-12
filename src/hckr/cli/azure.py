import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from yaspin import yaspin

from hckr.utils.AzureUtils import test_azure_connection, AzureConnectionTester
from hckr.utils.MessageUtils import PError



def common_azure_options(func):
    func = click.option("-t", "--tenant-id", help="Azure tenant ID", required=True)(
        func
    )
    func = click.option("-ci", "--client-id", help="Azure client ID (application ID)", required=True)(
        func
    )
    func = click.option("-cs", "--client-secret", help="Azure client secret", required=True, hide_input=True, prompt=True)(
        func
    )
    return func

@click.group(
    help="Azure commands",
    context_settings={"help_option_names": ["-h", "--help"]},
)
def azure():
    """Azure utility commands"""
    pass


@azure.command()
@common_azure_options
@click.option(
    "--subscription-id",
    help="Azure subscription ID (optional)",
)
@click.option(
    "--resource-group",
    help="Resource group name to test (optional)",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Show verbose output"
)
def test_connection(tenant_id, client_id, client_secret, subscription_id, resource_group, verbose):
    """
    Comprehensive Azure connection and permission testing.
    
    This command performs extensive validation including:
    
    **Authentication Validation**:
    * Credential format validation
    * Azure AD authentication test
    * Access token acquisition and validity check
    
    **Resource Access Validation** (when subscription-id provided):
    * Subscription access permissions
    * Resource group enumeration capabilities
    * Specific resource group access (when resource-group provided)
    
    **What is validated**:
    - Service principal authentication with Azure AD
    - Management API access permissions
    - Subscription-level read permissions
    - Resource group access permissions (if specified)
    
    Use `validate-credentials` for quick authentication-only testing.

    **Example Usage**:

    * Basic connection test:

    .. code-block:: shell

        $ hckr azure test-connection --tenant-id YOUR_TENANT_ID --client-id YOUR_CLIENT_ID

    * Test with subscription and resource group access:

    .. code-block:: shell

        $ hckr azure test-connection --tenant-id YOUR_TENANT_ID --client-id YOUR_CLIENT_ID --subscription-id YOUR_SUBSCRIPTION_ID --resource-group YOUR_RG

    **Command Reference**:
    """
    console = Console()
    
    with yaspin(text="Testing Azure connection...", color="blue", timer=True) as spinner:
        try:
            success, result = test_azure_connection(
                tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret,
                subscription_id=subscription_id,
                resource_group=resource_group
            )
            
            if success:
                spinner.ok("✔")
                
                # Create results table
                table = Table(title="Azure Connection Test Results", show_header=True)
                table.add_column("Property", style="cyan", no_wrap=True)
                table.add_column("Value", style="green")
                
                # Add basic info
                table.add_row("Overall Status", "✅ SUCCESS")
                table.add_row("Validation Summary", result["message"])
                table.add_row("Tenant ID", result["details"].get("tenant_id", "N/A"))
                table.add_row("Client ID", result["details"].get("client_id", "N/A"))
                table.add_row("Auth Method", result["details"].get("auth_method", "N/A"))
                
                # Authentication validation details
                table.add_row("─" * 20, "─" * 20)  # separator
                table.add_row("Authentication Tests", "PERFORMED")
                
                if "token_acquired" in result["details"]:
                    table.add_row("Token Acquired", "✅ Yes")
                    if "token_expires" in result["details"]:
                        import datetime
                        expires = datetime.datetime.fromtimestamp(result["details"]["token_expires"])
                        table.add_row("Token Expires", expires.strftime("%Y-%m-%d %H:%M:%S"))
                
                if subscription_id:
                    sub_access = result["details"].get("subscription_access", False)
                    table.add_row("Subscription Access", "✅ Yes" if sub_access else "❌ No")
                    if sub_access:
                        table.add_row("Subscription ID", result["details"].get("subscription_id", "N/A"))
                        rg_count = result["details"].get("resource_groups_count", 0)
                        table.add_row("Resource Groups Found", str(rg_count))
                        
                        if resource_group:
                            rg_access = result["details"].get("resource_group_access", False)
                            table.add_row("Resource Group Access", "✅ Yes" if rg_access else "❌ No")
                            if rg_access:
                                location = result["details"].get("resource_group_location", "N/A")
                                table.add_row("Resource Group Location", location)
                
                console.print(table)
                
                # Show verbose details if requested
                if verbose and result.get("details"):
                    console.print("\n[bold cyan]Detailed Information:[/bold cyan]")
                    for key, value in result["details"].items():
                        if key not in ["tenant_id", "client_id"]:  # Don't repeat sensitive info
                            console.print(f"  {key}: {value}")
                
            else:
                spinner.fail("✘")
                
                # Show error panel
                error_panel = Panel(
                    f"[red]❌ FAILED[/red]\n\n{result['message']}",
                    title="Azure Connection Test Failed",
                    border_style="red"
                )
                console.print(error_panel)
                
                if result.get("errors"):
                    console.print("\n[bold red]Errors:[/bold red]")
                    for error in result["errors"]:
                        console.print(f"  • {error}")
                
                if verbose and result.get("details"):
                    console.print("\n[bold cyan]Debug Information:[/bold cyan]")
                    for key, value in result["details"].items():
                        console.print(f"  {key}: {value}")
                
                # Exit with error code
                raise click.ClickException("Azure connection test failed")
                
        except Exception as e:
            spinner.fail("✘")
            PError(f"Connection test failed: {str(e)}")


@azure.command()
@common_azure_options
def validate_credentials(tenant_id, client_id, client_secret):
    """
    Quick validation of Azure service principal credentials (authentication only).
    
    This command performs the following validation steps:
    
    * **Credential Format Validation**: Verifies that tenant ID, client ID, and client secret are provided
    * **Azure AD Authentication**: Tests if the service principal can authenticate with Azure Active Directory
    * **Token Acquisition**: Validates that an access token can be successfully obtained
    * **Token Validity**: Confirms the token is valid and shows expiration time
    
    **What is NOT validated**:
    - Subscription access permissions
    - Resource group access permissions  
    - Specific Azure service permissions
    
    Use `test-connection` command for comprehensive testing including resource access.

    **Example Usage**:

    .. code-block:: shell

        $ hckr azure validate-credentials --tenant-id YOUR_TENANT_ID --client-id YOUR_CLIENT_ID

    **Command Reference**:
    """
    console = Console()
    
    with yaspin(text="Validating Azure credentials...", color="blue", timer=True) as spinner:
        try:
            tester = AzureConnectionTester()
            success, result = tester.test_connection_simple(
                tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret
            )
            
            if success:
                spinner.ok("✔")
                
                # Create detailed validation results table
                table = Table(title="Azure Credential Validation Results", show_header=True)
                table.add_column("Validation Step", style="cyan", no_wrap=True)
                table.add_column("Status", style="green")
                table.add_column("Details", style="yellow")
                
                # Add validation steps
                table.add_row("✅ Credential Format", "PASSED", "Tenant ID, Client ID, and Client Secret provided")
                table.add_row("✅ Azure AD Authentication", "PASSED", f"Service principal authenticated successfully")
                table.add_row("✅ Token Acquisition", "PASSED", "Access token obtained from Azure AD")
                
                if "token_expires" in result["details"]:
                    import datetime
                    expires = datetime.datetime.fromtimestamp(result["details"]["token_expires"])
                    table.add_row("✅ Token Validity", "PASSED", f"Token valid until {expires.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    table.add_row("✅ Token Validity", "PASSED", "Token is valid")
                
                console.print(table)
                console.print("\n[bold green]✅ All credential validation steps passed![/bold green]")
                console.print("[dim]Note: This validates authentication only. Use 'test-connection' for resource access validation.[/dim]")
            else:
                spinner.fail("✘")
                console.print(f"[red]❌ Invalid credentials: {result['message']}[/red]")
                if result.get("errors"):
                    for error in result["errors"]:
                        console.print(f"  • {error}")
                raise click.ClickException("Credential validation failed")
                
        except Exception as e:
            spinner.fail("✘")
            PError(f"Credential validation failed: {str(e)}")