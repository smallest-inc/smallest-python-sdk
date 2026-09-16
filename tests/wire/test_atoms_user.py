from .conftest import get_client, verify_request_count


def test_atoms_user_get_user_details() -> None:
    """Test getUserDetails endpoint with WireMock"""
    test_id = "atoms.user.get_user_details.0"
    client = get_client(test_id)
    client.atoms.user.get_user_details()
    verify_request_count(test_id, "GET", "/user", None, 1)


def test_atoms_user_get_subscription() -> None:
    """Test get_subscription endpoint with WireMock"""
    test_id = "atoms.user.get_subscription.0"
    client = get_client(test_id)
    client.atoms.user.get_subscription()
    verify_request_count(test_id, "GET", "/user/subscription", None, 1)
