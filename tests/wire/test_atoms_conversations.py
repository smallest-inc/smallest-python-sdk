from .conftest import get_client, verify_request_count


def test_atoms_conversations_get_a_time_limited_recording_download_url() -> None:
    """Test getATimeLimitedRecordingDownloadUrl endpoint with WireMock"""
    test_id = "atoms.conversations.get_a_time_limited_recording_download_url.0"
    client = get_client(test_id)
    client.atoms.conversations.get_a_time_limited_recording_download_url(
        call_id="CALL-1781127346211-e765f7",
    )
    verify_request_count(test_id, "GET", "/conversation/CALL-1781127346211-e765f7/recording/download-url", None, 1)


def test_atoms_conversations_list_retry_attempts() -> None:
    """Test list_retry_attempts endpoint with WireMock"""
    test_id = "atoms.conversations.list_retry_attempts.0"
    client = get_client(test_id)
    client.atoms.conversations.list_retry_attempts(
        call_id="callId",
    )
    verify_request_count(test_id, "GET", "/conversation/callId/retries", None, 1)


def test_atoms_conversations_cancel() -> None:
    """Test cancel endpoint with WireMock"""
    test_id = "atoms.conversations.cancel.0"
    client = get_client(test_id)
    client.atoms.conversations.cancel(
        call_id="CALL-1778226705739-7e4c17",
    )
    verify_request_count(test_id, "POST", "/conversation/cancel", None, 1)


def test_atoms_conversations_cancel_queued() -> None:
    """Test cancel_queued endpoint with WireMock"""
    test_id = "atoms.conversations.cancel_queued.0"
    client = get_client(test_id)
    client.atoms.conversations.cancel_queued(
        call_id="CALL-1781127346211-e765f7",
    )
    verify_request_count(test_id, "POST", "/conversation/CALL-1781127346211-e765f7/cancel", None, 1)
