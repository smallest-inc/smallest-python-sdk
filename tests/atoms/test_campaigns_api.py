import pytest
from smallestai.atoms.atoms_client import AtomsClient
from smallestai.atoms.models.create_campaign_request import CreateCampaignRequest
from smallestai.atoms.models.get_campaigns_request import GetCampaignsRequest
from smallestai.atoms.models.create_campaign201_response import CreateCampaign201Response
from smallestai.atoms.models.get_campaign_by_id200_response import GetCampaignById200Response
from smallestai.atoms.models.get_campaigns200_response import GetCampaigns200Response
from smallestai.atoms.models.delete_agent200_response import DeleteAgent200Response
import uuid

def test_create_campaign(atoms_client, global_state):
    campaign_name = f"Test {uuid.uuid4().hex[:8]}"
    request = CreateCampaignRequest(
        name=campaign_name,
        description="Test campaign description",
        agentId=global_state["base_agent"]["id"],
        audienceId=global_state["audience"]["id"]
    )
    
    response = atoms_client.create_campaign(create_campaign_request=request)
    
    assert isinstance(response, CreateCampaign201Response)

# def test_get_campaign_by_id(atoms_client, global_state):
#     # First create a campaign to get its ID
#     request = CreateCampaignRequest(
#         name="Test Campaign for Get",
#         description="Test campaign for get by ID",
#         agentId=global_state["base_agent"]["id"],
#         audienceId=global_state["audience"]["id"],
#         schedule={
#             "startTime": "2024-12-31T23:59:59Z",
#             "endTime": "2025-12-31T23:59:59Z",
#             "timezone": "UTC"
#         }
#     )
#     campaign = atoms_client.create_campaign(create_campaign_request=request)[0]
    
#     response = atoms_client.get_campaign_by_id(id=campaign.id)
#     assert isinstance(response, GetCampaignById200Response)

def test_get_campaigns(atoms_client):
    request = GetCampaignsRequest()
    response = atoms_client .get_campaigns(get_campaigns_request=request)
    assert isinstance(response, GetCampaigns200Response)

# def test_start_campaign(atoms_client, global_state):
#     response = atoms_client.start_campaign(id=global_state["campaign"]["id"])
#     assert isinstance(response, DeleteAgent200Response)

# def test_stop_campaign(atoms_client, global_state):
#     response = atoms_client.stop_campaign(id=global_state["campaign"]["id"])
#     assert isinstance(response, DeleteAgent200Response)

def test_delete_campaign(atoms_client, global_state):
    response = atoms_client.delete_campaign(id=global_state["campaign"]["id"])
    assert isinstance(response, DeleteAgent200Response) 