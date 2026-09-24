from .conftest import get_client, verify_request_count


def test_atoms_secrets_list_secrets() -> None:
    """Test list_secrets endpoint with WireMock"""
    test_id = "atoms.secrets.list_secrets.0"
    client = get_client(test_id)
    client.atoms.secrets.list_secrets()
    verify_request_count(test_id, "GET", "/secret", None, 1)


def test_atoms_secrets_create_secret() -> None:
    """Test create_secret endpoint with WireMock"""
    test_id = "atoms.secrets.create_secret.0"
    client = get_client(test_id)
    client.atoms.secrets.create_secret(
        name="ORDER_API_TOKEN",
        value="sk_live_xxxxxxxxxxxx",
    )
    verify_request_count(test_id, "POST", "/secret", None, 1)


def test_atoms_secrets_delete_secret() -> None:
    """Test delete_secret endpoint with WireMock"""
    test_id = "atoms.secrets.delete_secret.0"
    client = get_client(test_id)
    client.atoms.secrets.delete_secret(
        secret_id="secretId",
    )
    verify_request_count(test_id, "DELETE", "/secret/secretId", None, 1)
