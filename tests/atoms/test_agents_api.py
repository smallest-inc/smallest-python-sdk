import pytest
from smallestai.atoms.atoms_client import AtomsClient
from smallestai.atoms.models.create_agent_request import CreateAgentRequest
from smallestai.atoms.models.agent_id_patch_request import AgentIdPatchRequest
from smallestai.atoms.models.agent_from_template_post200_response import AgentFromTemplatePost200Response
from smallestai.atoms.models.agent_id_get200_response import AgentIdGet200Response
from smallestai.atoms.models.agent_get200_response import AgentGet200Response
from smallestai.atoms.models.agent_id_patch200_response import AgentIdPatch200Response
from smallestai.atoms.models.agent_id_delete200_response import AgentIdDelete200Response

def test_create_agent(atoms_client, global_state):
    request = CreateAgentRequest(
        name="Test Agent",
        description="Test agent description",
        # language={
        #     "enabled": "en",
        #     "synthesizer": {
        #         "voiceConfig": {
        #             "model": "waves_lightning_large",
        #             "voiceId": "nyah"
        #         },
        #         "speed": 1.2,
        #         "consistency": 0.5,
        #         "similarity": 0,
        #         "enhancement": 1
        #     },
        #     "speed": 1.2,
        #     "consistency": 0.5,
        #     "similarity": 0,
        #     "enhancement": 1
        # },
        slm_model="electron",
        global_knowledge_base_id=global_state["base_knowledge_base"]["id"]
    )
    
    response = atoms_client.create_agent(create_agent_request=request)
    assert isinstance(response, AgentFromTemplatePost200Response)

def test_get_agent_by_id(atoms_client, global_state):
    response = atoms_client.get_agent_by_id(id=global_state["base_agent"]["id"])
    assert isinstance(response, AgentIdGet200Response)

def test_get_agents(atoms_client):
    response = atoms_client.get_agents()
    assert isinstance(response, AgentGet200Response)

def test_update_agent(atoms_client, global_state):
    request = AgentIdPatchRequest(
        name="Updated Test Agent"
    )
    
    response = atoms_client.update_agent(
        id=global_state["base_agent"]["id"],
        agent_id_patch_request=request
    )
    assert isinstance(response, AgentIdPatch200Response)

def test_delete_agent(atoms_client, global_state):
    response = atoms_client.delete_agent(id=global_state["temp_agent"]["id"])
    assert isinstance(response, AgentIdDelete200Response)
