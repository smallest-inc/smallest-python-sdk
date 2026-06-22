from .conftest import get_client, verify_request_count

from smallestai.atoms import WidgetConfig


def test_atoms_agents_list_agents() -> None:
    """Test list_agents endpoint with WireMock"""
    test_id = "atoms.agents.list_agents.0"
    client = get_client(test_id)
    client.atoms.agents.list_agents()
    verify_request_count(test_id, "GET", "/agent", None, 1)


def test_atoms_agents_create_agent() -> None:
    """Test create_agent endpoint with WireMock"""
    test_id = "atoms.agents.create_agent.0"
    client = get_client(test_id)
    client.atoms.agents.create_agent(
        name="name",
    )
    verify_request_count(test_id, "POST", "/agent", None, 1)


def test_atoms_agents_get_agent() -> None:
    """Test get_agent endpoint with WireMock"""
    test_id = "atoms.agents.get_agent.0"
    client = get_client(test_id)
    client.atoms.agents.get_agent(
        id="id",
    )
    verify_request_count(test_id, "GET", "/agent/id", None, 1)


def test_atoms_agents_update_agent() -> None:
    """Test update_agent endpoint with WireMock"""
    test_id = "atoms.agents.update_agent.0"
    client = get_client(test_id)
    client.atoms.agents.update_agent(
        id="id",
    )
    verify_request_count(test_id, "PATCH", "/agent/id", None, 1)


def test_atoms_agents_archive_agent() -> None:
    """Test archive_agent endpoint with WireMock"""
    test_id = "atoms.agents.archive_agent.0"
    client = get_client(test_id)
    client.atoms.agents.archive_agent(
        id="id",
    )
    verify_request_count(test_id, "DELETE", "/agent/id/archive", None, 1)


def test_atoms_agents_duplicate_agent() -> None:
    """Test duplicate_agent endpoint with WireMock"""
    test_id = "atoms.agents.duplicate_agent.0"
    client = get_client(test_id)
    client.atoms.agents.duplicate_agent(
        id="id",
        target_organization_id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "POST", "/agent/id/duplicate", None, 1)


def test_atoms_agents_get_agent_workflow() -> None:
    """Test getAgentWorkflow endpoint with WireMock"""
    test_id = "atoms.agents.get_agent_workflow.0"
    client = get_client(test_id)
    client.atoms.agents.get_agent_workflow(
        id="id",
    )
    verify_request_count(test_id, "GET", "/agent/id/workflow", None, 1)


def test_atoms_agents_update_workflow_configuration() -> None:
    """Test update_workflow_configuration endpoint with WireMock"""
    test_id = "atoms.agents.update_workflow_configuration.0"
    client = get_client(test_id)
    client.atoms.agents.update_workflow_configuration(
        id="60d0fe4f5311236168a109ca",
        type="workflow_graph",
    )
    verify_request_count(test_id, "PATCH", "/workflow/60d0fe4f5311236168a109ca", None, 1)


def test_atoms_agents_create_with_ai() -> None:
    """Test create_with_ai endpoint with WireMock"""
    test_id = "atoms.agents.create_with_ai.0"
    client = get_client(test_id)
    client.atoms.agents.create_with_ai()
    verify_request_count(test_id, "POST", "/agent/with-ai", None, 1)


def test_atoms_agents_list_call_logs() -> None:
    """Test list_call_logs endpoint with WireMock"""
    test_id = "atoms.agents.list_call_logs.0"
    client = get_client(test_id)
    client.atoms.agents.list_call_logs(
        id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "GET", "/agent/60d0fe4f5311236168a109ca/call-logs", None, 1)


def test_atoms_agents_get_widget_config() -> None:
    """Test get_widget_config endpoint with WireMock"""
    test_id = "atoms.agents.get_widget_config.0"
    client = get_client(test_id)
    client.atoms.agents.get_widget_config(
        id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "GET", "/agent/60d0fe4f5311236168a109ca/widget-config", None, 1)


def test_atoms_agents_update_widget_config() -> None:
    """Test update_widget_config endpoint with WireMock"""
    test_id = "atoms.agents.update_widget_config.0"
    client = get_client(test_id)
    client.atoms.agents.update_widget_config(
        id="60d0fe4f5311236168a109ca",
        widget_config=WidgetConfig(),
    )
    verify_request_count(test_id, "PATCH", "/agent/60d0fe4f5311236168a109ca/widget-config", None, 1)


def test_atoms_agents_get_prompt_config() -> None:
    """Test get_prompt_config endpoint with WireMock"""
    test_id = "atoms.agents.get_prompt_config.0"
    client = get_client(test_id)
    client.atoms.agents.get_prompt_config()
    verify_request_count(test_id, "GET", "/agent/prompt-config", None, 1)
