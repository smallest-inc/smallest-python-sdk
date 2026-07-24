from .conftest import get_client, verify_request_count


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


def test_atoms_agents_duplicate_agent() -> None:
    """Test duplicate_agent endpoint with WireMock"""
    test_id = "atoms.agents.duplicate_agent.0"
    client = get_client(test_id)
    client.atoms.agents.duplicate_agent(
        id="id",
        target_organization_id="60d0fe4f5311236168a109ca",
    )
    verify_request_count(test_id, "POST", "/agent/id/duplicate", None, 1)


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


def test_atoms_agents_get_agent_widget_config() -> None:
    """Test getAgentWidgetConfig endpoint with WireMock"""
    test_id = "atoms.agents.get_agent_widget_config.0"
    client = get_client(test_id)
    client.atoms.agents.get_agent_widget_config(
        id="id",
    )
    verify_request_count(test_id, "GET", "/agent/id/widget-config", None, 1)


def test_atoms_agents_update_agent_widget_config() -> None:
    """Test updateAgentWidgetConfig endpoint with WireMock"""
    test_id = "atoms.agents.update_agent_widget_config.0"
    client = get_client(test_id)
    client.atoms.agents.update_agent_widget_config(
        id="id",
    )
    verify_request_count(test_id, "PATCH", "/agent/id/widget-config", None, 1)


def test_atoms_agents_get_agent_avatar_presigned_url() -> None:
    """Test getAgentAvatarPresignedUrl endpoint with WireMock"""
    test_id = "atoms.agents.get_agent_avatar_presigned_url.0"
    client = get_client(test_id)
    client.atoms.agents.get_agent_avatar_presigned_url(
        id="id",
        file_name="fileName",
        content_type="contentType",
        file_size=1.1,
    )
    verify_request_count(test_id, "POST", "/agent/id/avatar/presigned-url", None, 1)


def test_atoms_agents_get_agent_call_logs() -> None:
    """Test getAgentCallLogs endpoint with WireMock"""
    test_id = "atoms.agents.get_agent_call_logs.0"
    client = get_client(test_id)
    client.atoms.agents.get_agent_call_logs(
        id="id",
    )
    verify_request_count(test_id, "GET", "/agent/id/call-logs", None, 1)


def test_atoms_agents_archive_agent() -> None:
    """Test archive_agent endpoint with WireMock"""
    test_id = "atoms.agents.archive_agent.0"
    client = get_client(test_id)
    client.atoms.agents.archive_agent(
        id="id",
    )
    verify_request_count(test_id, "DELETE", "/agent/id/archive", None, 1)
