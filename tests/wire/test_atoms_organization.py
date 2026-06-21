from .conftest import get_client, verify_request_count


def test_atoms_organization_get_organization_details() -> None:
    """Test getOrganizationDetails endpoint with WireMock"""
    test_id = "atoms.organization.get_organization_details.0"
    client = get_client(test_id)
    client.atoms.organization.get_organization_details()
    verify_request_count(test_id, "GET", "/organization", None, 1)


def test_atoms_organization_get_account_details() -> None:
    """Test get_account_details endpoint with WireMock"""
    test_id = "atoms.organization.get_account_details.0"
    client = get_client(test_id)
    client.atoms.organization.get_account_details()
    verify_request_count(test_id, "GET", "/account/get-account-details", None, 1)


def test_atoms_organization_update_name() -> None:
    """Test update_name endpoint with WireMock"""
    test_id = "atoms.organization.update_name.0"
    client = get_client(test_id)
    client.atoms.organization.update_name(
        name="name",
    )
    verify_request_count(test_id, "PUT", "/account/update-org-name", None, 1)
