from .conftest import get_client, verify_request_count

from smallestai.agents.call_actions import CreateCallActionRequestConfig


def test_atoms_callActions_list_call_actions() -> None:
    """Test listCallActions endpoint with WireMock"""
    test_id = "atoms.call_actions.list_call_actions.0"
    client = get_client(test_id)
    client.agents.call_actions.list_call_actions(
        agent_id="agentId",
    )
    verify_request_count(test_id, "GET", "/call-actions", {"agentId": "agentId"}, 1)


def test_atoms_callActions_create_call_action() -> None:
    """Test createCallAction endpoint with WireMock"""
    test_id = "atoms.call_actions.create_call_action.0"
    client = get_client(test_id)
    client.agents.call_actions.create_call_action(
        agent_id="agentId",
        category="trigger",
        provider="provider",
        config=CreateCallActionRequestConfig(),
    )
    verify_request_count(test_id, "POST", "/call-actions", None, 1)


def test_atoms_callActions_get_call_action() -> None:
    """Test getCallAction endpoint with WireMock"""
    test_id = "atoms.call_actions.get_call_action.0"
    client = get_client(test_id)
    client.agents.call_actions.get_call_action(
        id="id",
    )
    verify_request_count(test_id, "GET", "/call-actions/id", None, 1)


def test_atoms_callActions_update_call_action() -> None:
    """Test updateCallAction endpoint with WireMock"""
    test_id = "atoms.call_actions.update_call_action.0"
    client = get_client(test_id)
    client.agents.call_actions.update_call_action(
        id="id",
    )
    verify_request_count(test_id, "PUT", "/call-actions/id", None, 1)


def test_atoms_callActions_delete_call_action() -> None:
    """Test deleteCallAction endpoint with WireMock"""
    test_id = "atoms.call_actions.delete_call_action.0"
    client = get_client(test_id)
    client.agents.call_actions.delete_call_action(
        id="id",
    )
    verify_request_count(test_id, "DELETE", "/call-actions/id", None, 1)
