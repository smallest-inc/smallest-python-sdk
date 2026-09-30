from .conftest import get_client, verify_request_count


def test_atoms_agentTelephony_list_answers() -> None:
    """Test list_answers endpoint with WireMock"""
    test_id = "atoms.agent_telephony.list_answers.0"
    client = get_client(test_id)
    client.atoms.agent_telephony.list_answers(
        agent_id="agentId",
    )
    verify_request_count(test_id, "GET", "/agent/agentId/answers", None, 1)


def test_atoms_agentTelephony_attach_answer() -> None:
    """Test attach_answer endpoint with WireMock"""
    test_id = "atoms.agent_telephony.attach_answer.0"
    client = get_client(test_id)
    client.atoms.agent_telephony.attach_answer(
        agent_id="agentId",
        source_kind="phoneNumber",
        source_id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "POST", "/agent/agentId/answers", None, 1)


def test_atoms_agentTelephony_detach_answer() -> None:
    """Test detach_answer endpoint with WireMock"""
    test_id = "atoms.agent_telephony.detach_answer.0"
    client = get_client(test_id)
    client.atoms.agent_telephony.detach_answer(
        agent_id="agentId",
        source_id="sourceId",
    )
    verify_request_count(test_id, "DELETE", "/agent/agentId/answers/sourceId", None, 1)


def test_atoms_agentTelephony_list_caller_ids() -> None:
    """Test list_caller_ids endpoint with WireMock"""
    test_id = "atoms.agent_telephony.list_caller_ids.0"
    client = get_client(test_id)
    client.atoms.agent_telephony.list_caller_ids(
        agent_id="agentId",
    )
    verify_request_count(test_id, "GET", "/agent/agentId/caller-ids", None, 1)


def test_atoms_agentTelephony_attach_caller_id() -> None:
    """Test attach_caller_id endpoint with WireMock"""
    test_id = "atoms.agent_telephony.attach_caller_id.0"
    client = get_client(test_id)
    client.atoms.agent_telephony.attach_caller_id(
        agent_id="agentId",
        source_kind="phoneNumber",
        source_id="sourceId",
    )
    verify_request_count(test_id, "POST", "/agent/agentId/caller-ids", None, 1)


def test_atoms_agentTelephony_detach_caller_id() -> None:
    """Test detach_caller_id endpoint with WireMock"""
    test_id = "atoms.agent_telephony.detach_caller_id.0"
    client = get_client(test_id)
    client.atoms.agent_telephony.detach_caller_id(
        agent_id="agentId",
        source_id="sourceId",
        number="number",
    )
    verify_request_count(test_id, "DELETE", "/agent/agentId/caller-ids/sourceId", {"number": "number"}, 1)


def test_atoms_agentTelephony_set_transfer_source() -> None:
    """Test set_transfer_source endpoint with WireMock"""
    test_id = "atoms.agent_telephony.set_transfer_source.0"
    client = get_client(test_id)
    client.atoms.agent_telephony.set_transfer_source(
        agent_id="agentId",
    )
    verify_request_count(test_id, "PUT", "/agent/agentId/transfer-source", None, 1)
