import datetime

from .conftest import get_client, verify_request_count


def test_atoms_calls_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "atoms.calls.list_.0"
    client = get_client(test_id)
    client.atoms.calls.list(
        agent_ids="60d0fe4f5311236168a109ca,60d0fe4f5311236168a109cb",
        campaign_ids="60d0fe4f5311236168a109ca,60d0fe4f5311236168a109cb",
        search="+1234567890",
        status_filter="completed,failed",
        disconnect_reason_filter="user_hangup,agent_hangup",
        call_attempt_filter="initial",
        duration_filter="0-30,30-60",
        date_from=datetime.datetime.fromisoformat("2025-01-01T00:00:00+00:00"),
        date_to=datetime.datetime.fromisoformat("2025-01-31T23:59:59+00:00"),
    )
    verify_request_count(
        test_id,
        "GET",
        "/conversation",
        {
            "agentIds": "60d0fe4f5311236168a109ca,60d0fe4f5311236168a109cb",
            "campaignIds": "60d0fe4f5311236168a109ca,60d0fe4f5311236168a109cb",
            "search": "+1234567890",
            "statusFilter": "completed,failed",
            "disconnectReasonFilter": "user_hangup,agent_hangup",
            "callAttemptFilter": "initial",
            "durationFilter": "0-30,30-60",
            "dateFrom": "2025-01-01T00:00:00Z",
            "dateTo": "2025-01-31T23:59:59Z",
        },
        1,
    )


def test_atoms_calls_search() -> None:
    """Test search endpoint with WireMock"""
    test_id = "atoms.calls.search.0"
    client = get_client(test_id)
    client.atoms.calls.search(
        call_ids=["CALL-1737000000000-abc123", "CALL-1737000000001-def456"],
    )
    verify_request_count(test_id, "POST", "/conversation/search", None, 1)


def test_atoms_calls_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "atoms.calls.get.0"
    client = get_client(test_id)
    client.atoms.calls.get(
        id="CALL-1737000000000-abc123",
    )
    verify_request_count(test_id, "GET", "/conversation/CALL-1737000000000-abc123", None, 1)


def test_atoms_calls_start_outbound_call() -> None:
    """Test start_outbound_call endpoint with WireMock"""
    test_id = "atoms.calls.start_outbound_call.0"
    client = get_client(test_id)
    client.atoms.calls.start_outbound_call(
        agent_id="60d0fe4f5311236168a109ca",
        phone_number="+1234567890",
    )
    verify_request_count(test_id, "POST", "/conversation/outbound", None, 1)
