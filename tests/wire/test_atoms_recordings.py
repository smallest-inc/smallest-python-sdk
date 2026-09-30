from .conftest import get_client, verify_request_count


def test_atoms_recordings_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "atoms.recordings.get.0"
    client = get_client(test_id)
    client.atoms.recordings.get(
        call_id="CALL-1781127346211-e765f7",
    )
    verify_request_count(test_id, "GET", "/recordings/CALL-1781127346211-e765f7", None, 1)
