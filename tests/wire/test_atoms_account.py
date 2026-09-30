from .conftest import get_client, verify_request_count


def test_atoms_account_get_account_details() -> None:
    """Test getAccountDetails endpoint with WireMock"""
    test_id = "atoms.account.get_account_details.0"
    client = get_client(test_id)
    client.atoms.account.get_account_details()
    verify_request_count(test_id, "GET", "/account/get-account-details", None, 1)


def test_atoms_account_update_organization_name() -> None:
    """Test updateOrganizationName endpoint with WireMock"""
    test_id = "atoms.account.update_organization_name.0"
    client = get_client(test_id)
    client.atoms.account.update_organization_name(
        name="Acme Inc.",
    )
    verify_request_count(test_id, "PUT", "/account/update-org-name", None, 1)
