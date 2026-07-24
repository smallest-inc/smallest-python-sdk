from .conftest import get_client, verify_request_count

from smallestai.atoms import WebEngageIntegrationSet


def test_atoms_integrations_modify_web_engage_integration() -> None:
    """Test modifyWebEngageIntegration endpoint with WireMock"""
    test_id = "atoms.integrations.modify_web_engage_integration.0"
    client = get_client(test_id)
    client.atoms.integrations.modify_web_engage_integration(
        integration_sets=[
            WebEngageIntegrationSet(
                license_code="licenseCode",
                environment="environment",
                api_key="apiKey",
            )
        ],
    )
    verify_request_count(test_id, "POST", "/integration/modify-webengage-integration", None, 1)


def test_atoms_integrations_get_web_engage_details() -> None:
    """Test getWebEngageDetails endpoint with WireMock"""
    test_id = "atoms.integrations.get_web_engage_details.0"
    client = get_client(test_id)
    client.atoms.integrations.get_web_engage_details()
    verify_request_count(test_id, "GET", "/integration/get-webengage-details", None, 1)
