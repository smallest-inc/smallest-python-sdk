from .conftest import get_client, verify_request_count


def test_atoms_calls_start_an_outbound_call() -> None:
    """Test startAnOutboundCall endpoint with WireMock"""
    test_id = "atoms.calls.start_an_outbound_call.0"
    client = get_client(test_id)
    client.atoms.calls.start_an_outbound_call(
        agent_id="60d0fe4f5311236168a109ca",
        phone_number="+1234567890",
    )
    verify_request_count(test_id, "POST", "/conversation/outbound", None, 1)
