import pytest
from smallestai.atoms.atoms_client import AtomsClient
from smallestai.atoms.models.create_agent_request import CreateAgentRequest
from smallestai.atoms.models.update_agent_request import UpdateAgentRequest
from smallestai.atoms.models.create_agent_from_template200_response import CreateAgentFromTemplate200Response
from smallestai.atoms.models.get_agent_by_id200_response import GetAgentById200Response
from smallestai.atoms.models.get_agents200_response import GetAgents200Response
from smallestai.atoms.models.update_agent200_response import UpdateAgent200Response
from smallestai.atoms.models.delete_agent200_response import DeleteAgent200Response


def test_create_agent(atoms_client, global_state):
    request = CreateAgentRequest(
        name="Test Agent",
        description="Test agent description",
        language={
            "enabled": "en",
            "switching": False
        },
        synthesizer={
            "voiceConfig": {
                "model": "waves_lightning_large",
                "voiceId": "nyah"
            },
            "speed": 1.2,
            "consistency": 0.5,
            "similarity": 0,
            "enhancement": 1
        },
        slmModel="electron-v1",
        globalKnowledgeBaseId=global_state["base_knowledge_base"]["id"]
    )
    
    response = atoms_client.create_agent(create_agent_request=request)
    assert isinstance(response, CreateAgentFromTemplate200Response)

def test_get_agent_by_id(atoms_client, global_state):
    response = atoms_client.get_agent_by_id(id=global_state["base_agent"]["id"])
    assert isinstance(response, GetAgentById200Response)

def test_get_agents(atoms_client):
    response = atoms_client.get_agents()
    assert isinstance(response, GetAgents200Response)

def test_update_agent(atoms_client, global_state):
    request = UpdateAgentRequest(
        name="Updated Test Agent"
    )
    
    response = atoms_client.update_agent(
        id=global_state["base_agent"]["id"],
        update_agent_request=request
    )
    assert isinstance(response, UpdateAgent200Response)

def test_delete_agent(atoms_client, global_state):
    response = atoms_client.delete_agent(id=global_state["temp_agent"]["id"])
    assert isinstance(response, DeleteAgent200Response)
