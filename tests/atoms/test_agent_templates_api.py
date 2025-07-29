import pytest
from smallestai.atoms.atoms_client import AtomsClient
from smallestai.atoms.models.agent_template_get200_response import AgentTemplateGet200Response
from smallestai.atoms.models.agent_from_template_post200_response import AgentFromTemplatePost200Response
from smallestai.atoms.models.create_agent_from_template_request import CreateAgentFromTemplateRequest

def test_get_agent_templates(atoms_client, global_state):
    """Test getting list of agent templates"""
    response = atoms_client.get_agent_templates()
    assert isinstance(response, AgentTemplateGet200Response)

def test_create_agent_from_template(atoms_client, global_state):
    """Test creating an agent from a template"""
    
    request = CreateAgentFromTemplateRequest(
        templateId=global_state["base_agent_template"]["id"],
        agentName="Test Template Agent",
        agentDescription="Agent created from template for testing"
    )
    
    response = atoms_client.create_agent_from_template(create_agent_from_template_request=request)
    assert isinstance(response, AgentFromTemplatePost200Response) 