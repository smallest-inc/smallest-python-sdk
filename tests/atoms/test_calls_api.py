import pytest
from smallestai.atoms.atoms_client import AtomsClient
from smallestai.atoms.models.start_outbound_call_request import StartOutboundCallRequest
from smallestai.atoms.models.start_outbound_call200_response import StartOutboundCall200Response

def test_start_outbound_call(atoms_client, global_state):
    """Test starting an outbound call"""
    
    request = StartOutboundCallRequest(
        agentId=global_state["base_agent"]["id"],
        phoneNumber="+919769384457",
    )
    
    response = atoms_client.start_outbound_call(start_outbound_call_request=request)
    print(response)
    
    assert isinstance(response, StartOutboundCall200Response) 