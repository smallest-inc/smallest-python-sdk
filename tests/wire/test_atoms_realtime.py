from .conftest import get_client, verify_request_count


def test_atoms_realtime_register_call() -> None:
    """Test register_call endpoint with WireMock"""
    test_id = "atoms.realtime.register_call.0"
    client = get_client(test_id)
    client.agents.realtime.register_call(
        agent_id="69da0b4c20c0e03cfa4ee258",
    )
    verify_request_count(test_id, "POST", "/conversation/register-call", None, 1)
