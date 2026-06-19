from .conftest import get_client, verify_request_count


def test_atoms_liveTranscripts_subscribe_to_live_events() -> None:
    """Test subscribe_to_live_events endpoint with WireMock"""
    test_id = "atoms.live_transcripts.subscribe_to_live_events.0"
    client = get_client(test_id)
    for _ in client.atoms.live_transcripts.subscribe_to_live_events(
        call_id="CALL-1758124225863-80752e",
    ):
        pass
    verify_request_count(test_id, "GET", "/events", {"callId": "CALL-1758124225863-80752e"}, 1)
