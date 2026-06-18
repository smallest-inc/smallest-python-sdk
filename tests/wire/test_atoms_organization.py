from .conftest import get_client, verify_request_count


def test_atoms_organization_get_organization_details() -> None:
    """Test getOrganizationDetails endpoint with WireMock"""
    test_id = "atoms.organization.get_organization_details.0"
    client = get_client(test_id)
    client.atoms.organization.get_organization_details()
    verify_request_count(test_id, "GET", "/organization", None, 1)
