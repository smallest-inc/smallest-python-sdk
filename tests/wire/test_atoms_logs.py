from .conftest import get_client, verify_request_count


def test_atoms_logs_get_all_conversation_logs() -> None:
    """Test getAllConversationLogs endpoint with WireMock"""
    test_id = "atoms.logs.get_all_conversation_logs.0"
    client = get_client(test_id)
    client.atoms.logs.get_all_conversation_logs(
        agent_ids="60d0fe4f5311236168a109ca,60d0fe4f5311236168a109cb",
        campaign_ids="60d0fe4f5311236168a109ca,60d0fe4f5311236168a109cb",
        search="+1234567890",
        status_filter="completed,failed",
        disconnect_reason_filter="user_hangup,agent_hangup",
        call_attempt_filter="initial",
        duration_filter="0-30,30-60",
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
        },
        1,
    )


def test_atoms_logs_search_conversation_logs_by_call_i_ds() -> None:
    """Test searchConversationLogsByCallIDs endpoint with WireMock"""
    test_id = "atoms.logs.search_conversation_logs_by_call_i_ds.0"
    client = get_client(test_id)
    client.atoms.logs.search_conversation_logs_by_call_i_ds(
        call_ids=["CALL-1737000000000-abc123", "CALL-1737000000001-def456"],
    )
    verify_request_count(test_id, "POST", "/conversation/search", None, 1)


def test_atoms_logs_get_conversation_log_by_id() -> None:
    """Test getConversationLogById endpoint with WireMock"""
    test_id = "atoms.logs.get_conversation_log_by_id.0"
    client = get_client(test_id)
    client.atoms.logs.get_conversation_log_by_id(
        id="CALL-1737000000000-abc123",
    )
    verify_request_count(test_id, "GET", "/conversation/CALL-1737000000000-abc123", None, 1)
