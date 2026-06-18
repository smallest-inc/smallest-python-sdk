from .conftest import get_client, verify_request_count


def test_atoms_liveTranscripts_subscribe_to_live_call_events_sse() -> None:
    """Test subscribeToLiveCallEventsSse endpoint with WireMock"""
    test_id = "atoms.live_transcripts.subscribe_to_live_call_events_sse.0"
    client = get_client(test_id)
    for _ in client.atoms.live_transcripts.subscribe_to_live_call_events_sse(
        call_id="CALL-1758124225863-80752e",
    ):
        pass
    verify_request_count(test_id, "GET", "/events", {"callId": "CALL-1758124225863-80752e"}, 1)
