import pytest
from smallestai.atoms.atoms_client import AtomsClient
from smallestai.atoms.models.create_agent_from_template_request import CreateAgentFromTemplateRequest
from smallestai.atoms.models.get_agent_templates200_response import GetAgentTemplates200Response
from smallestai.atoms.models.create_agent_from_template200_response import CreateAgentFromTemplate200Response

def test_get_agent_templates(atoms_client, global_state):
    """Test getting list of agent templates"""
    response = atoms_client.get_agent_templates()
    assert isinstance(response, GetAgentTemplates200Response)

def test_create_agent_from_template(atoms_client, global_state):
    """Test creating an agent from a template"""
    
    request = CreateAgentFromTemplateRequest(
        templateId=global_state["base_agent_template"]["id"],
        agentName="Test Template Agent",
        agentDescription="Agent created from template for testing"
    )
    
    response = atoms_client.create_agent_from_template(create_agent_from_template_request=request)
    assert isinstance(response, CreateAgentFromTemplate200Response) 