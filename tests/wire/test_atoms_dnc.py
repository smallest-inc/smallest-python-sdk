from .conftest import get_client, verify_request_count


def test_atoms_dnc_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "atoms.dnc.list_.0"
    client = get_client(test_id)
    client.atoms.dnc.list()
    verify_request_count(test_id, "GET", "/dnc", None, 1)
