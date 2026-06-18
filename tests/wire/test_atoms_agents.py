from .conftest import get_client, verify_request_count


def test_atoms_agents_get_all_agents() -> None:
    """Test getAllAgents endpoint with WireMock"""
    test_id = "atoms.agents.get_all_agents.0"
    client = get_client(test_id)
    client.atoms.agents.get_all_agents()
    verify_request_count(test_id, "GET", "/agent", None, 1)


def test_atoms_agents_create_a_new_agent() -> None:
    """Test createANewAgent endpoint with WireMock"""
    test_id = "atoms.agents.create_a_new_agent.0"
    client = get_client(test_id)
    client.atoms.agents.create_a_new_agent(
        name="name",
    )
    verify_request_count(test_id, "POST", "/agent", None, 1)


def test_atoms_agents_get_agent_by_id() -> None:
    """Test getAgentById endpoint with WireMock"""
    test_id = "atoms.agents.get_agent_by_id.0"
    client = get_client(test_id)
    client.atoms.agents.get_agent_by_id(
        id="id",
    )
    verify_request_count(test_id, "GET", "/agent/id", None, 1)


def test_atoms_agents_update_agent_metadata() -> None:
    """Test updateAgentMetadata endpoint with WireMock"""
    test_id = "atoms.agents.update_agent_metadata.0"
    client = get_client(test_id)
    client.atoms.agents.update_agent_metadata(
        id="id",
    )
    verify_request_count(test_id, "PATCH", "/agent/id", None, 1)


def test_atoms_agents_delete_agent() -> None:
    """Test deleteAgent endpoint with WireMock"""
    test_id = "atoms.agents.delete_agent.0"
    client = get_client(test_id)
    client.atoms.agents.delete_agent(
        id="id",
    )
    verify_request_count(test_id, "DELETE", "/agent/id/archive", None, 1)


def test_atoms_agents_duplicate_agent_to_another_organization() -> None:
    """Test duplicateAgentToAnotherOrganization endpoint with WireMock"""
    test_id = "atoms.agents.duplicate_agent_to_another_organization.0"
    client = get_client(test_id)
    client.atoms.agents.duplicate_agent_to_another_organization(
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
    """Test updateWorkflowConfiguration endpoint with WireMock"""
    test_id = "atoms.agents.update_workflow_configuration.0"
    client = get_client(test_id)
    client.atoms.agents.update_workflow_configuration(
        id="60d0fe4f5311236168a109ca",
        type="workflow_graph",
    )
    verify_request_count(test_id, "PATCH", "/workflow/60d0fe4f5311236168a109ca", None, 1)
