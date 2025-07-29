import pytest
from smallestai.atoms.atoms_client import AtomsClient
from smallestai.atoms.models.campaign_post_request import CampaignPostRequest
from smallestai.atoms.models.campaign_get_request import CampaignGetRequest
from smallestai.atoms.models.campaign_post201_response import CampaignPost201Response
from smallestai.atoms.models.campaign_id_get200_response import CampaignIdGet200Response
from smallestai.atoms.models.campaign_get200_response import CampaignGet200Response
from smallestai.atoms.models.agent_id_delete200_response import AgentIdDelete200Response
import uuid

def test_create_campaign(atoms_client, global_state):
    request = CampaignPostRequest(
        name="Test Campaign",
        description="Test campaign description",
        agentId=global_state["base_agent"]["id"],
        audienceId=global_state["audience"]["id"]
    )
    response = atoms_client.create_campaign(campaign_post_request=request)
    assert isinstance(response, CampaignPost201Response)  # Returns List[CampaignPost201Response]

def test_get_campaigns(atoms_client):
    request = CampaignGetRequest()
    response = atoms_client.get_campaigns(campaign_get_request=request)
    assert isinstance(response, CampaignGet200Response)

def test_get_campaign_by_id(atoms_client, global_state):
    response = atoms_client.get_campaign_by_id(id=global_state["base_campaign"]["id"])
    assert isinstance(response, CampaignIdGet200Response)

def test_start_campaign(atoms_client, global_state):
    response = atoms_client.start_campaign(id=global_state["base_campaign"]["id"])
    assert isinstance(response, AgentIdDelete200Response)

def test_pause_campaign(atoms_client, global_state):
    response = atoms_client.pause_campaign(id=global_state["base_campaign"]["id"])
    assert isinstance(response, AgentIdDelete200Response)

def test_delete_campaign(atoms_client, global_state):
    response = atoms_client.delete_campaign(id=global_state["temp_campaign"]["id"])
    assert isinstance(response, AgentIdDelete200Response) 