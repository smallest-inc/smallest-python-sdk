from .conftest import get_client, verify_request_count


def test_atoms_agentTemplates_list_agent_templates() -> None:
    """Test list_agent_templates endpoint with WireMock"""
    test_id = "atoms.agent_templates.list_agent_templates.0"
    client = get_client(test_id)
    client.atoms.agent_templates.list_agent_templates()
    verify_request_count(test_id, "GET", "/agent/template", None, 1)


def test_atoms_agentTemplates_create_agent_from_template() -> None:
    """Test createAgentFromTemplate endpoint with WireMock"""
    test_id = "atoms.agent_templates.create_agent_from_template.0"
    client = get_client(test_id)
    client.atoms.agent_templates.create_agent_from_template(
        agent_name="agentName",
        template_id="templateId",
    )
    verify_request_count(test_id, "POST", "/agent/from-template", None, 1)
